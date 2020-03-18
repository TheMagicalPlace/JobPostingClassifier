import time
from collections import defaultdict
import json
import logging

from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

import os




class IndeedClient:

    def __init__(self,search_term,file_term):
        """Sets up the requisite instance variables for the scraoper

        search_term - the term to be searched on Indeed
        file_term - the corresponding folder that results should be written to

        The distinction is to allow for variations on the same term to be grouped together, i.e. 'Chemical Engineer'
        and 'Entry Level Chemical Engineer' are two seperate search terms, but results from both should be considered
        together when classifying and/or writing search results."""

        # if the folder name is the same as the search term
        if file_term != search_term:
            self.search_term = search_term
            self.file_term = file_term
            try:
                with open(os.path.join(os.getcwd(),file_term,'jobs_data'),'r') as jobs:
                    self.jobinfo = json.loads(jobs.read())
            except FileNotFoundError:
                self.jobinfo = {}
        # for related search terms
        else:
            self.search_term = search_term
            self.file_term = self.search_term
            try:
                with open(os.path.join(os.getcwd(),self.file_term,'jobs_data'),'r') as jobs:
                    self.jobinfo = json.loads(jobs.read())
            except FileNotFoundError:
                self.jobinfo = {}
        # how many more jobs to find is based on last + jobs to find
        self.last_length = len(self.jobinfo.keys())


    def __call__(self,location='United States',jobs_to_find=100):

        # length of job dict with new jobs added
        self.next_length = self.last_length+jobs_to_find
        job_desc = self.search_term
        self.to_find = jobs_to_find
        self.driver_startup()
        self.navigate_to_jobs(job_desc,location)
        self.navigate_through_pages(job_desc)
        self.driver.close()

    def driver_startup(self):
        """launches the webdriver & navigated to indeed homepage"""
        self.driver = webdriver.Chrome('/home/themagicalplace/Documents/chromedriver')
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

    def get_jobs_on_page(self,desc):
        """Gets job info for each unseen job on the current page"""

        elem = self.driver.find_elements_by_class_name('title')
        containers = self.driver.find_elements_by_class_name('jobsearch-SerpJobCard')
        seen = []
        for ele,container in zip(elem,containers):

            # exits once target no. of jobs are found
            if self.last_length >= self.next_length:
                print('exited')
                break

            # hiring events aren't jobs and break the scraper
            if 'Hiring Event' in ele.text:
                continue

            base = container.get_attribute('id')
            xpath = f"//div[@id = {base}]/table/tbody/tr/td/span"
            #print(xpath,ele.text)

            try:
                ele.click()
            except ElementClickInterceptedException:
                ele.send_keys(Keys.ESCAPE)
                ele.click()

            # HTML element id's
            link_id = "jobtitle"
            job_id = "vjs-jobtitle"
            company_id = "vjs-cn"
            location_id = "vjs-loc"
            desc_id = "vjs-desc"

            # waiting for each panel to load
            try:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, desc_id)))
            except TimeoutException:
                continue


            n = self.driver.find_element_by_id(job_id).text
            e = self.driver.find_elements_by_partial_link_text(n)

            # multiple jobs can have the same title, in this case the link used is the first link for the sanem
            # job title that has not been seen
            if len(e) > 1:
                for lnk in e:
                    lnk = lnk.get_attribute("href")
                    if lnk in seen:
                        continue
                    else:
                        seen.append(lnk)
                        link = lnk
                        break
            elif len(e) == 0 : continue
            else:
                link = e[0].get_attribute("href")


            info = {
                'link' : link,
                'job name':self.driver.find_element_by_id(job_id).text,
                'company' : self.driver.find_element_by_id(company_id).text,
                'location' : self.driver.find_element_by_id(location_id).text,
                'description' : self.driver.find_element_by_id(desc_id).text,
                'date_posted' : 'n/a'
                    }
            hash_string = info['job name']+' - '+info['company']
            self.jobinfo[hash_string] = info

            self.last_length +=1
        self.save_jobs()

    def navigate_through_pages(self,job_desc):
        """Navigates from page to page of the job search results"""
        i = 0
        while self.last_length < self.next_length:
            # wait for the page to load
            try:
                WebDriverWait(self.driver,60).until(
                    EC.element_to_be_clickable(
                        (By.PARTIAL_LINK_TEXT,'Next'))
                )
            except TimeoutException:
                print('Exited on Page ' + str(i))
                break

            # closes out any on-page popups
            self.driver.find_element_by_partial_link_text('Next').send_keys(Keys.ESCAPE)

            #get job data
            self.get_jobs_on_page(job_desc)

            self.driver.find_element_by_partial_link_text('Next').click()
            time.sleep(3)
            i +=1


    def save_jobs(self):
        """saves the jobs to the corresponding json file"""
        with open(os.path.join(os.getcwd(),self.file_term,'jobs_data'),'w') as job:
            d = json.dumps(self.jobinfo)
            job.write(d)

if __name__ == '__main__':

    test1 = IndeedClient('Chemical Engineer','Chemical Engineer')
    test1(jobs_to_find=1)