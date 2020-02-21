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
from selenium.common.exceptions import TimeoutException
import os




class IndeedClient:

    def __init__(self,search_term):
        try:
            with open(os.path.join(os.getcwd(),search_term,'jobs_data'),'r') as jobs:
                self.jobinfo = json.loads(jobs.read())
        except FileNotFoundError:
            self.jobinfo = {}
        finally:
            self.search_term = search_term


    def __call__(self,location='United States',jobs_to_find=100):
        #display = Xvfb()
        #display.start()
        job_desc = self.search_term
        self.to_find = jobs_to_find
        self.driver_startup()
        self.navigate_to_jobs(job_desc,location)
        self.navigate_through_pages(job_desc)
        self.driver.close()

    def driver_startup(self):
        self.driver = webdriver.Chrome('/home/themagicalplace/Documents/chromedriver')
        self.driver.get('https://www.indeed.com/')


    def navigate_to_jobs(self,job_desc,location='United States'):

        try:
            self.jobinfo[job_desc]
        except KeyError:
            self.jobinfo[job_desc] ={}
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

        #WebDriverWait(self.driver,120).until(EC.element_to_be_clickable((By.ID,job_id)))
        elem = self.driver.find_elements_by_class_name('title')
        for ele in elem:
            if len(self.jobinfo[desc].keys()) >= self.to_find:
                print('exited')
                break

            ele.click()
            link_id = "jobtitle"
            job_id = "vjs-jobtitle"
            company_id = "vjs-cn"
            location_id = "vjs-loc"
            desc_id = "vjs-desc"

            try:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, desc_id)))
            except TimeoutException:
                continue
            info = {
                'link' : self.driver.find_element_by_class_name(link_id).get_attribute("href"),
                'job name':self.driver.find_element_by_id(job_id).text,
                'company' : self.driver.find_element_by_id(company_id).text,
                'location' : self.driver.find_element_by_id(location_id).text,
                'description' : self.driver.find_element_by_id(desc_id).text,
                'date_posted' : 'n/a'
                    }
            hash_string = info['job name']+' - '+info['company']
            (self.jobinfo[desc])[hash_string] = info

        self.save_jobs()

    def navigate_through_pages(self,job_desc):
        i = 0
        while len(self.jobinfo[job_desc].keys()) < self.to_find:
            print('\n')
            print('page ' + str(i))
            print('\n')

            try:
                WebDriverWait(self.driver,60).until(
                    EC.element_to_be_clickable(
                        (By.PARTIAL_LINK_TEXT,'Next'))
                )
            except TimeoutException:
                continue
            self.driver.find_element_by_partial_link_text('Next').send_keys(Keys.ESCAPE)
            self.get_jobs_on_page(job_desc)
            self.driver.find_element_by_partial_link_text('Next').click()
            time.sleep(3)
            print('page yeet')
            i +=1

    def save_jobs(self):
        with open(os.path.join(os.getcwd(),self.search_term,'jobs_data'),'w') as job:
            d = json.dumps(self.jobinfo)
            job.write(d)

#vjs-footer > div.result-link-bar-container.result-link-bar-viewjob > div > span.date.date-a11y
if __name__ == '__main__':

    test1 = IndeedClient('Chemical Engineer')
    test1(jobs_to_find=10)