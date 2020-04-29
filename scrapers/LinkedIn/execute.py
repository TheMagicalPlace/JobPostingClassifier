import json


import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import time
from scrapers.LinkedIn.scrape import ScraperLinkdin as

class skeys:
    search_keys = {
        "username"         :  "chris621@msu.edu",
        "password"         :  "Istanbul1453",
        "keywords"         :  ["Chemical Engineer"],
        "locations"        :  ["United States"],

        # specify the search radius from 'location' in miles:
        #    '10', '25', '35', '50', '75', '100'
        "search_radius"    :  "50",

        # go to page number in results. Helps if an error occurred in a
        # previous attempt, user can pick up where left off. Set it
        # to '1' if no results page number need be specified.
        "results_page"      :  1,

        # specify date range: 'All',  '1',  '2-7',  '8-14',  '15-30'
        "date_range"       :  "All",

        # sort by either 'Relevance' or 'Date Posted'
        "sort_by"          :  "Date Posted",

        # specify salary range: 'All', '40+', '60+', '80+', '100+', '120+', '140+', '160+', '180+', '200+'
        "salary_range"     :  "All",

        # data is written to file in working directory as filename
        "filename"         :  "output.txt"
}


if __name__ == '__main__':
    driver = webdriver.Chrome('C:\\Users\\17344\\Documents\\chromedriver')
    driver.get("https://www.linkedin.com/uas/login")
    driver.maximize_window()
    client = LIClient(driver, **skeys.search_keys)
    client.login()
    driver.get("https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=Chemical%20Engineer&location=United%20States")
    client.navigate_search_results()
    client.driver_quit()