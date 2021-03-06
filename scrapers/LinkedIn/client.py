
from __future__ import print_function

import os
import re
import sqlite3
import time
from collections import Counter

import selenium
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scrapers.LinkedIn.scrape import ScraperLinkdin as _ScraperLinkedin
from scrapers.driver_version_checker import driverversionchecker


class LIClient():
    def __init__(self, search_term,file_term,location,jobs_to_find):
        # TODO generalize webdriver path
        self.location = location
        self.jobs_to_find = jobs_to_find
        self.search_term = search_term
        self.file_term = file_term

        self.scrape_continue = True
        self.location = location
        self.page = 1

    def driver_startup(self):
        """launches the webdriver & navigated to Indeed homepage"""
        self.driver = driverversionchecker()
        self.scraper = _ScraperLinkedin(self.driver,
                                        self.database,
                                        search_term=self.search_term,
                                        no_of_calls=self.jobs_to_find)
        self.driver.get('https://www.linkedin.com/')
        self.driver.maximize_window()

    def __call__(self, username,password):
        self.database = sqlite3.connect(os.path.join(os.getcwd(), self.file_term, f'{self.file_term}.db'))
        self.driver_startup()
        self.login(username,password)
        self.navigate_to_jobs_page()
        self.enter_search_keys()
        self.navigate_search_results()

    def driver_quit(self):
        self.driver.quit()

    def login(self,username,password):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.PARTIAL_LINK_TEXT, "Sign in")
                )
            )
        except:
            pass
        else:
            self.driver.find_element_by_link_text("Sign in").click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.ID, "username")
                )
            )

        except:
            print("ERROR in finding username in")
            #elem = self.driver.find_element_by_xpath("//*[text()='Email or Phone']")
        else:
            time.sleep(1)
            elem = self.driver.find_element_by_id("username")
            elem.send_keys(username)
            time.sleep(1)
            elem = self.driver.find_element_by_id("password")
            elem.send_keys(password)
            time.sleep(1)
        # Enter credentials with Keys.RETURN
        self.driver.find_element_by_xpath("//button[text()='Sign in']").click()

        # checking for update info popup
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[text()='Skip']")
                )
            )
        except:
            pass
        else:
            self.driver.find_element_by_xpath( "//button[text()='Skip']").click()
        # Wait a few seconds for the page to load

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
            try:
                id = re.findall(r"(?<=ember)[0-9]+",input)[0]
            except IndexError:
                pass
            else:
                input = driver.find_element_by_id(input)
                if input.get_attribute('id') == f'jobs-search-box-keyword-id-ember{id}':
                    input.send_keys(self.search_term)
                elif input.get_attribute('id') == f'jobs-search-box-location-id-ember{id}':
                    input.send_keys(self.location)
                time.sleep(0.1)
        self.driver.find_element_by_xpath("//button[text()='Search']").click()

    def next_results_page(self):
        """
        navigate to the next page of search results. If an error is encountered
        then the process ends or new search criteria are entered as the current
        search results may have been exhausted.
        """
        try:
            # wait for the next page button to load
            print("  Moving to the next page of search results... \n" \
                  "  If search results are exhausted, will wait {} seconds " \
                  "then either execute new search or quit".format(10))
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//button/span[text()='{self.page}']")
                )
            )
            # navigate to next page
            actions = ActionChains(self.driver)

            btn = self.driver.find_element_by_xpath(f"//button/span[text()='{self.page}']")
            actions.move_to_element_with_offset(btn, 0, 0).perform()
            btn.click()
        except selenium.common.exceptions.TimeoutException:
            actions = ActionChains(self.driver)
            btn = self.driver.find_element_by_xpath(f"//button/span[text()='…']")
            actions.move_to_element_with_offset(btn, 0, 0).perform()
            btn.click()
        except Exception as e:
            print("\nFailed to click next page link; Search results " \
                  "may have been exhausted\n{}".format(e))
            raise ValueError("Next page link not detected; search results exhausted")

    def navigate_search_results(self):
        """
        scrape postings for all pages in search results
        """
        driver = self.driver
        scraper = self.scraper
        search_results_exhausted = False
        results_page = 1
        delay = 60
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-search-results__list")
                )
            )
        except selenium.common.exceptions.TimeoutException:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "jobs-search-two-pane__results")
                )
            )

        # css elements to view job pages
        list_element_tag = '/descendant::a[@class="job-card-search__link-wrapper js-focusable disabled ember-view"]['
        #print_num_search_results(driver, self.keyword, self.location)
        # go to a specific results page number if one is specified
        #go_to_specific_results_page(driver, delay, results_page)
        results_page = results_page if results_page > 1 else 1

        #while not search_results_exhausted:
        while not search_results_exhausted:
            lnks = []
            link1 = self.driver.find_element_by_class_name("jobs-search-results")
            link1.send_keys(Keys.END)
            time.sleep(0.5)
            link1.send_keys(Keys.HOME)
            time.sleep(3)
            links = self.driver.find_elements_by_xpath(
                """//ul[contains(concat(' ',normalize-space(@class),' '),'jobs-search-results__list')]//*//
                a[contains(concat(' ',normalize-space(@class),' '),'job-card-list__title')]""")

            for l in links:
                cls = l.get_attribute('class').split()
                if ("job-card-search__link-wrapper" in cls or "job-card-container__link" in cls) \
                and l.get_attribute('id') not in lnks and l.text != '':
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
            self.page +=1
            try:
                self.next_results_page()
                print("\n**************************************************")
                print("\n\n\nNavigating to results page  {}" \
                      "\n\n\n".format(results_page + 1))
            except ValueError:
                search_results_exhausted = True
                print("**************************************************")
                print("\n\n\n\n\nSearch results exhausted\n\n\n\n\n")
            else:
                results_page += 1



