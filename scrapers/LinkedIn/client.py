
from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapers.LinkedIn.scrape import ScraperLinkdin as _ScraperLinkedin
import datetime
import os
import json
import time
from collections import Counter
from selenium.webdriver.common.action_chains import ActionChains



class LIClient(object):
    def __init__(self, search_term,file_term,location,jobs_to_find):
        # TODO generalize webdriver path
        self.driver         =  webdriver.Chrome('/home/themagicalplace/Documents/chromedriver')
        self.location = location
        self.jobs_to_find = jobs_to_find
        self.search_term = search_term
        self.file_term = file_term
        self.database = os.path.join(os.getcwd(),file_term,f'{file_term}.db')
        self.scrape_continue = True
        self.location = location

    def driver_startup(self):
        """launches the webdriver & navigated to indeed homepage"""
        # TODO configure driver info
        self.driver = webdriver.Chrome('/home/themagicalplace/Documents/chromedriver')
        self.scraper = _ScraperLinkedin(self.driver,
                                        self.database,
                                        search_term=self.search_term,
                                        no_of_calls=self.jobs_to_find)
        self.driver.get('https://www.linkedin.com/')


    def __call__(self, username,password):
        self.driver_startup()
        self.login(username,password)
        self.navigate_to_jobs_page()
        self.navigate_search_results()

    def driver_quit(self):
        self.driver.quit()

    def login(self,username,password):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable(
                (By.ID, "username")
            )
        )
        elem = self.driver.find_element_by_id("username")
        elem.send_keys(username)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait a few seconds for the page to load
        time.sleep(3)

    def navigate_to_jobs_page(self):
        """
        navigate to the 'Jobs' page since it is a convenient page to
        enter a custom job search.
        """
        # Click the Jobs search page
        jobs_link_clickable = False
        attempts = 1
        url = "https://www.linkedin.com/jobs/?trk=nav_responsive_sub_nav_jobs"
        while not jobs_link_clickable:
            try:
                self.driver.get(url)
            except Exception as e:
                attempts += 1
                if attempts > 10**3:
                    print("  jobs page not detected")
                    break
                pass
            else:
                print("**************************************************")
                print ("\n\n\nSuccessfully navigated to jobs search page\n\n\n")
                jobs_link_clickable = True

    def enter_search_keys(self):
        """
        execute the job search by entering job and location information.
        The location is pre-filled with text, so we must clear it before
        entering our search.
        """
        driver = self.driver
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "jobs-search-box__text-input")
            )
        )
        # Enter search criteria
        ins =driver.find_elements_by_tag_name('input')
        ins = [inn.get_attribute('id') for inn in ins if inn.get_attribute('id').strip()]

        for input in ins:

            input = driver.find_element_by_id(input)
            if input.get_attribute('aria-label') == 'Search jobs':
                input.send_keys(self.search_term)
            elif input.get_attribute('aria-label') == 'Search location':
                input.send_keys(self.location)
        input.send_keys(Keys.RETURN)
        time.sleep(3)

    def next_results_page(self, delay):
        """
        navigate to the next page of search results. If an error is encountered
        then the process ends or new search criteria are entered as the current
        search results may have been exhausted.
        """
        try:
            # wait for the next page button to load
            print("  Moving to the next page of search results... \n" \
                  "  If search results are exhausted, will wait {} seconds " \
                  "then either execute new search or quit".format(delay))
            WebDriverWait(self.driver, delay).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.next-btn")
                )
            )
            # navigate to next page
            self.driver.find_element_by_css_selector("a.next-btn").click()
        except Exception as e:
            print("\nFailed to click next page link; Search results " \
                  "may have been exhausted\n{}".format(e))
            raise ValueError("Next page link not detected; search results exhausted")
        else:
            # wait until the first job post button has loaded
            first_job_button = "a.job-title-link"
            # wait for the first job post button to load
            WebDriverWait(self.driver, delay).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, first_job_button)
                )
            )

    def navigate_search_results(self):
        """
        scrape postings for all pages in search results
        """
        driver = self.driver
        scraper = self.scraper
        search_results_exhausted = False
        results_page = 1
        delay = 60
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "job-card-search__link-wrapper")
            )
        )
        time.sleep(2)

        # css elements to view job pages
        list_element_tag = '/descendant::a[@class="job-card-search__link-wrapper js-focusable disabled ember-view"]['
        #print_num_search_results(driver, self.keyword, self.location)
        # go to a specific results page number if one is specified
        #go_to_specific_results_page(driver, delay, results_page)
        results_page = results_page if results_page > 1 else 1

        #while not search_results_exhausted:
        while not search_results_exhausted:
            lnks = []
            link1 = self.driver.find_element_by_class_name("job-card-search__link-wrapper")
            link1.send_keys(Keys.END)
            time.sleep(0.5)
            link1.send_keys(Keys.HOME)
            links = self.driver.find_elements_by_tag_name('a')

            for l in links:
                cls = l.get_attribute('class').split()
                if "job-card-search__link-wrapper" in cls and l.get_attribute('id') not in lnks and l.text != '':
                    lnks.append(l.text)
                    actions = ActionChains(driver)
                   # driver.execute_script('arguments[0].scrollIntoView(true);', l)
                    actions.move_to_element_with_offset(l,0,0).perform()
                    time.sleep(0.05)


            print(lnks)
            cnt = Counter(lnks)
            for name,count in cnt.items():
                link_elems = driver.find_elements_by_link_text(name)
                for i in range(count):
                    elem = link_elems[i]
                    self.scrape_continue = scraper.scrape_page(elem)
                    if not self.scrape_continue:
                        return
            # attempt to navigate to the next page of search results
            # if the link is not present, then the search results have been
            # exhausted
            try:
                self.next_results_page(delay)
                print("\n**************************************************")
                print("\n\n\nNavigating to results page  {}" \
                      "\n\n\n".format(results_page + 1))
            except ValueError:
                search_results_exhausted = True
                print("**************************************************")
                print("\n\n\n\n\nSearch results exhausted\n\n\n\n\n")
            else:
                results_page += 1



