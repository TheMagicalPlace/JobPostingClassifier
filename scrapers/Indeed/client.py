import os
import time
import sqlite3
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import scrapers
from scrapers import driver_version_checker



#TODO normalize file terms for scraper and program
class IndeedClient:

    def __init__(self,search_term,file_term,location,jobs_to_find):


        """Sets up the requisite instance variables for the scraoper

        search_term - the term to be searched on Indeed
        file_term - the corresponding folder that results should be written to

        The distinction is to allow for variations on the same term to be grouped together, i.e. 'Chemical Engineer'
        and 'Entry Level Chemical Engineer' are two seperate search terms, but results from both should be considered
        together when classifying and/or writing search results."""

        self.location = location
        self.jobs_to_find = jobs_to_find
        self.search_term = search_term
        self.file_term = file_term
        self.scrape_continue = True

    def __call__(self):
        self.database = sqlite3.connect(os.path.join(os.getcwd(), self.file_term, f'{self.file_term}.db'))
        self.driver_startup()
        self.navigate_to_jobs(self.search_term,self.location)
        self.navigate_through_pages()
        self.driver.close()

    def driver_startup(self):
        """launches the webdriver & navigated to indeed homepage"""


        self.driver = scrapers._driverversionchecker()

        self.scraper =scrapers._ScraperIndeed(self.driver,
                                              database=self.database,
                                              search_term=self.search_term,
                                              no_of_calls=self.jobs_to_find,
                                              file_path_args=self.file_term)
        self.driver.get('https://www.indeed.com/')

    def navigate_to_jobs(self,job_desc,location='United States'):
        """ Inputs search term + location and navigates to results"""

        WebDriverWait(self.driver,120).until(EC.element_to_be_clickable((By.ID,'text-input-what')))
        elem = self.driver.find_element_by_id('text-input-what')
        elem.send_keys(job_desc)
        elem = self.driver.find_element_by_id('text-input-where')
        elem.send_keys(Keys.CONTROL+'a')
        elem.send_keys(Keys.DELETE)
        elem.send_keys(location)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

    def get_jobs_on_page(self):
        """Gets job info for each unseen job on the current page"""

        elem = self.driver.find_elements_by_class_name('title')
        containers = self.driver.find_elements_by_class_name('jobsearch-SerpJobCard')
        for ele,container in zip(elem,containers):

            # exits once target no. of jobs are found
            if not self.scrape_continue:
                print('exited')
                break

            # hiring events aren't jobs and break the scraper
            if 'Hiring Event' in ele.text:
                continue

            base = container.get_attribute('id')
            xpath = f"//div[@id = {base}]/table/tbody/tr/td/span"
            #print(xpath,ele.text)


            # handling popups on page
            try:
                ele.click()
            except ElementClickInterceptedException:
                a = self.driver.switch_to.alert()
                a.dismiss()
                ele.click()

            # waiting for each panel to load
            try:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, "vjs-desc")))
            except TimeoutException:
                continue

            # scraping job data , exits if the scraper sends False
            self.scrape_continue = self.scraper.scrape_page(ele)
            if not self.scrape_continue:
                return

    def navigate_through_pages(self):
        """Navigates from page to page of the job search results"""
        i = 0
        self.selector = None
        while self.scrape_continue:
            i += 1
            # wait for the page to load



            try:
                WebDriverWait(self.driver,15).until(
                    EC.element_to_be_clickable(
                        (By.PARTIAL_LINK_TEXT,'Next'))
                )
                # closes out any on-page popups
                self.driver.find_element_by_partial_link_text('Next').send_keys(Keys.ESCAPE)
            except TimeoutException:
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[@aria-label='Next']"))
                    )
                    # closes out any on-page popups
                    self.driver.find_element_by_xpath("//a[@aria-label='Next']").send_keys(Keys.ESCAPE)
                except TimeoutException:
                    print('Exited on Page ' + str(i))
                    break
                else:
                    self.get_jobs_on_page()
                    self.driver.find_element_by_xpath("//a[@aria-label='Next']").click()
            else:
                self.get_jobs_on_page()
                self.driver.find_element_by_partial_link_text('Next').click()
            finally:
                time.sleep(3)

if __name__ == '__main__':
    client = IndeedClient("operator","operator","United States",10)
    client()