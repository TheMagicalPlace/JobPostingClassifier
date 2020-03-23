from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import time
from scraper_template import *
import re


class ScraperLinkdin(ScraperBase):

    def get_link(self,element):
        return element.get_attribute('href')


    def get_job_name(self,element):
        return element.text


    def get_company_name(self,element):
        element.click()
        return self.driver.find_element_by_css_selector("a.jobs-details-top-card__company-url").text


    def get_job_location(self,*args):
        return self.driver.find_element_by_class_name("jobs-details-top-card__bullet").text


    def get_description(self,*args):
        return self.driver.find_element_by_id("job-details").text


    def get_post_date(self,*args):
        return ""



