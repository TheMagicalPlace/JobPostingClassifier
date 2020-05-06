import json
import os
import sys
from collections import defaultdict

from selenium import webdriver
from selenium.common.exceptions import *


def driverversionchecker():


    with open(os.path.join(os.getcwd(), 'user_information', 'settings.json'), 'r+') as data:
        settings = json.loads(data.read())
        setdict = defaultdict(dict, settings)

        if not setdict['driver_version']:
            setdict['driver_version'] = {'browser':None,'version':''}
            driver,browser,version = set_driver_version()
            setdict['driver_version'] = {'browser':browser,'version':version}
            data.seek(0)
            data.write(json.dumps(setdict))
        else:
            try:
                driver_info = setdict['driver_version']
                if driver_info['browser'] == 'firefox':

                    if sys.platform == 'win32':
                        driver = webdriver.Firefox(
                            executable_path=os.path.join(os.getcwd(), 'webdrivers', 'geckodriver', driver_info['version'],
                                                         'geckodriver.exe'))
                    else:
                        driver = webdriver.Firefox(
                            executable_path=os.path.join(os.getcwd(), 'webdrivers', 'geckodriver', driver_info['version'],
                                                         'geckodriver'))
                else:
                    if sys.platform == 'win32':
                        driver = webdriver.Chrome(
                            executable_path=os.path.join(os.getcwd(), 'webdrivers', 'chromedriver',
                                                         driver_info['version'],
                                                         'chromedriver.exe'))
                    else:

                        driver = webdriver.Chrome(
                        executable_path=os.path.join(os.getcwd(), 'webdrivers', 'chromedriver', driver_info['version'],
                                             'chromedriver'))
                driver.get("https://www.google.com")
            except WebDriverException:
                driver,browser, version = set_driver_version()
                setdict['driver_version'] = {'browser': browser, 'version': version}
                data.seek(0)
                data.write(json.dumps(setdict))
    return driver

def set_driver_version():
    version_try_order=[]
    version_order=[]
    for i,drivers in enumerate(['chromedriver','geckodriver']):
        vers = []
        for j,ver in enumerate(sorted([ _.name.split('.') for _ in os.scandir(os.path.join(os.getcwd(),'webdrivers',drivers))],
                                      key = lambda version : int(version[1]) if version[0][0] == 'v' else int(version[0]))):
            version_try_order.insert(i+2*j,".".join(ver))


    while version_try_order:
        version_order.append((version_try_order.pop(),version_try_order.pop()))
    print(version_order)

    for versions in version_order:
        try:
            if sys.platform == 'win32':
                driver = webdriver.Firefox(executable_path=os.path.join(os.getcwd(), 'webdrivers', 'geckodriver',versions[0],'geckodriver.exe'))
            else:
                driver = webdriver.Firefox(
                    executable_path=os.path.join(os.getcwd(), 'webdrivers', 'geckodriver', versions[0],
                                                 'geckodriver'))
            driver.get("https://www.google.com")

        except WebDriverException as e:
            print(e)
            try:
                if sys.platform == 'win32':
                    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'webdrivers', 'chromedriver',versions[1],'chromedriver.exe'))
                else:
                    driver = webdriver.Chrome(
                        executable_path=os.path.join(os.getcwd(), 'webdrivers', 'chromedriver', versions[1],
                                                     'chromedriver'))
                driver.get("https://www.google.com")

            except WebDriverException as e:
                print(e)
                continue
            else:
                return driver,"chrome",versions[1]
        else:
            return driver,'firefox',versions[0]
