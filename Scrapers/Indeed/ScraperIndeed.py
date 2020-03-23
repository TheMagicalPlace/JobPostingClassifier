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
from Scrapers import scraper_template



class ScraperIndeed(scraper_template.ScraperBase):
    link_id = "jobtitle"
    job_id = "vjs-jobtitle"
    company_id = "vjs-cn"
    location_id = "vjs-loc"
    desc_id = "vjs-desc"

    def __init__(self,driver,save_every=10,file_path_args=()):
        super().__init__(driver,save_every=save_every,file_path_args=())
        self.seen = []


    def get_link(self,element):
        n = self.driver.find_element_by_id(self.job_id).text
        e = self.driver.find_elements_by_partial_link_text(n)
        if len(e) > 1:
            for lnk in e:
                lnk = lnk.get_attribute("href")
                if lnk in self.seen:
                    continue
                else:
                    self.seen.append(lnk)
                    link = lnk
                    break
        elif len(e) == 0:
            return "Link Not Found!"
        else:
            link = e[0].get_attribute("href")

        return link


    def get_job_name(self,*args):
        return self.driver.find_element_by_id("vjs-jobtitle").text

    def get_company_name(self,*args):
        return self.driver.find_element_by_id(self.company_id).text

    def get_job_location(self,*args):
        return self.driver.find_element_by_id(self.location_id).text,

    def get_description(self,*args):
        return self.driver.find_element_by_id(self.desc_id).text


    def get_post_date(self,*args):
        return ""

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

