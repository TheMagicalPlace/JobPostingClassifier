from zipfile import ZipFile
import requests
import bs4
import re
import sys,os
import urllib3
import tqdm
import tarfile
from abc import ABC,abstractmethod

class UnsupportedOSError(Exception):
    def __init__(self,driver):
        self.message =f"""Unsupported operating system '{sys.platform}' detected, either try and install {driver}
                            manually or use this application on a different operating system"""
        super().__init__(self.message)

class DriverManagerABC(ABC):
    """Base class for webdriver downloaders. Impliments universal methods for saving data, downloading
    the drivers, and an abstract method for getting driver-specific download links."""

    def __init__(self,driver_id):
        self.driver_id = driver_id
        self._http_pool = urllib3.PoolManager()
        self.download_links = []
        self.versions = []

        # each driver type is saved under its own file path
        self.file_path = os.path.join(os.getcwd(),"webdrivers",self.driver_id)
        pass

    def download_drivers(self):
        self.get_download_links()
        for ver,lnk in zip(self.versions,self.download_links):
            self.save_data(ver,lnk)

    def save_data(self, version, dl_link):
        """Method for saving the downloaded driver to the appropriate location."""
        driver_obj = self._http_pool.request('GET',dl_link,preload_content=False)
        with open(os.path.join(os.getcwd(), self.file_path,f"{self.driver_id}{version}.zip"), 'wb') as driver:
            for chunk in tqdm.tqdm(driver_obj.stream(32)):
                driver.write(chunk)
        driver_obj.release_conn()
        self._unpack_files(version)

    def _unpack_files(self,version):
        """Method for handling zip file downloads."""
        zip_obj = ZipFile(os.path.join(os.getcwd(), self.file_path, f"{self.driver_id}{version}.zip"), mode='r')
        zip_obj.infolist()
        zip_obj.extractall(path=os.path.join(os.getcwd(), self.file_path, version))
        zip_obj.close()
        os.remove(os.path.join(os.getcwd(), self.file_path, f"{self.driver_id}{version}.zip"))

    @abstractmethod
    def get_download_links(self):
        """Abstract method for handling the navigation of the download site for each driver. Responsible
        for scraping the download links and handling version checking."""
        pass

class DriverManagerChrome(DriverManagerABC):
    def __init__(self):
        super().__init__(driver_id='chromedriver')

    def get_download_links(self):
        base_url_chromedriver = 'https://chromedriver.chromium.org/downloads'
        basepage = requests.get(base_url_chromedriver)
        bs_soup = bs4.BeautifulSoup(basepage.text, 'html.parser')
        links = bs_soup.find_all("a", string=re.compile(r"ChromeDriver [0-9.]+"))

        for lnk in links[:3]:
            path = re.findall(r"(?<=path=)[0-9.]+",lnk['href'])
            if sys.platform == 'win32':
                dl_link = f'https://chromedriver.storage.googleapis.com/{path[0]}/chromedriver_win32.zip'
            elif sys.platform == 'linux':
                dl_link = f'https://chromedriver.storage.googleapis.com/{path[0]}/chromedriver_linux64.zip'
            elif sys.platform == 'darwin':
                dl_link = f'https://chromedriver.storage.googleapis.com/{path[0]}/chromedriver_mac64.zip'
            else:
                raise UnsupportedOSError("ChromeDriver")
            self.download_links.append(dl_link)
            self.versions.append(path[0])

class DriverManagerFirefox(DriverManagerABC):
    def __init__(self):
        super().__init__(driver_id='geckodriver')

    def get_download_links(self):
        base_url_geckodriver = 'https://github.com/mozilla/geckodriver/releases'
        basepage = requests.get(base_url_geckodriver)
        bs_soup = bs4.BeautifulSoup(basepage.text, 'html.parser')
        links = bs_soup.find_all("a", string=re.compile(r"v[0-9.]+"))
        for lnk in links[:3]:
            path = re.findall(r"v[0-9.]+", lnk['href'])

            if sys.platform == 'win32':
                dl_link = f"https://github.com/mozilla/geckodriver/releases/download/{path[0]}/geckodriver-{path[0]}-win32.zip"
            elif sys.platform == 'linux':
                dl_link = f"https://github.com/mozilla/geckodriver/releases/download/{path[0]}/geckodriver-{path[0]}-linux64.tar.gz"
            elif sys.platform == 'darwin':
                dl_link = f"https://github.com/mozilla/geckodriver/releases/download/{path[0]}/geckodriver-{path[0]}-macos.tar.gz"
            else:
                raise UnsupportedOSError("ChromeDriver")
            self.download_links.append(dl_link)
            self.versions.append(path[0])

    def _unpack_files(self,version):
        """Geckodriver downloads can also come as tar.gz files for non-windows systems, so this method overwrites
        the one found in the base class to account for the different file types."""
        if sys.platform == 'win32':
            super()._unpack_files(version)
        else:
            tarfile_obj = tarfile.TarFile(os.path.join(os.getcwd(), self.file_path, f"{self.driver_id}{version}.tar.gz"))
            tarfile_obj.extractall(path=os.path.join(os.getcwd(), self.file_path, version))
            tarfile_obj.close()
            os.remove(os.path.join(os.getcwd(), self.file_path, f"{self.driver_id}{version}.tar.gz"))

if __name__ == '__main__':
    d = DriverManagerFirefox()
    d.download_drivers()
    d = DriverManagerChrome()
    d.download_drivers()
