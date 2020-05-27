#TODO check out why occasional hangs on 1st job page

import abc
import json
import os
import re
import sqlite3
import time
from datetime import timedelta
from typing import Iterable


class ScraperBase(abc.ABC):
    """Abstract base class for all of my job board web scrapers"""


    time_ago_re = re.compile(r"([0-9]+)[+]?( days? ago)")

    def __init__(self,driver,database,search_term,no_of_calls,file_path_args : Iterable[str] = ()):
        self.driver = driver
        self.search_term = search_term
        self.job_dict = {}     # Holds each job posting
        self.calls = no_of_calls         # calls made to the scraper
        self.fpargs = file_path_args
        self.database = database

    def format_time(self,post_time : str):

        res = re.match(ScraperBase.time_ago_re,post_time)
        if res:
            return res[0]

        time_formats = ['%d %b %y',     # i.e. 30 Nov 00
                        '%d %m %Y',     # i.e 3 31 2020
                        '%d-%m-%Y',     # i.e 3-31-2020
                        '%d/%m/%Y',     # i.e 3/31/2020
                        '%Y-%m-%d',     # i.e 2020-3-31 31
                        ]

        for formt in time_formats:
            try:
                post_date = time.strptime(formt,post_time)
                return post_time
            except ValueError:
                continue
        else:
            print("No valid date format found")
            return "NA"

    def depreciated_save_data_json(self,fpargs):
        print(os.path.join(os.getcwd(),fpargs,"jobs_data.json"))
        jpath = os.path.join(os.getcwd(),*fpargs,"jobs_data.json")
        if os.path.exists(jpath):
            with open(os.path.join(os.getcwd(),*fpargs,"jobs_data.json"),'r+') as jobdat:
                print(self.fpargs)
                self.job_dict.update(json.loads(jobdat.read()))
                jobdat.write(json.dumps(self.job_dict))
        else:
            with open(os.path.join(os.getcwd(),*fpargs,"job_data.json"),'w') as jobdat:
                jobdat.write(json.dumps(self.job_dict))

    def scrape_page(self, element):
        """
        scrapes single job page after the driver loads a new job posting and saves to a database
        """

        # wait ~1 second for elements to be dynamically rendered
        time.sleep(0.2)
        start = time.time()

        link = re.sub("[-|;]","_",self.get_link(element))
        job_name = self.get_job_name(element)
        company = str(self.get_company_name(element))
        location = str(self.get_job_location(element))

        description = str(self.get_description(element))
        post_date=self.format_time(self.get_post_date(element))
        post_date = post_date if not isinstance(post_date, time.struct_time) \
                              else timedelta(time.time(), self.format_time(self.get_post_date(element)))
        job_uid = "_".join([job_name,company,location])

        try:
            with self.database as db:
                cur = db.cursor()
                cur.execute("INSERT INTO metadata VALUES (?,?,?,?,?,?)",(job_uid,self.search_term,link,location,company,post_date))

        except sqlite3.IntegrityError:
            print('Operational Error with job insert or Job already in Table')
        else:
            with self.database as cdb:
                cur = cdb.cursor()
                cur.execute("INSERT INTO unsorted VALUES (?,?,?)", (job_uid, job_name, description))
            self.calls-=1
        if self.calls <= 0:
            return False
        else:
            return True

    @abc.abstractmethod
    def get_link(self,*args):
        pass

    @abc.abstractmethod
    def get_job_name(self,*args):
        pass

    @abc.abstractmethod
    def get_company_name(self,*args):
        pass

    @abc.abstractmethod
    def get_job_location(self,*args):
        pass

    @abc.abstractmethod
    def get_description(self,*args):
        pass

    @abc.abstractmethod
    def get_post_date(self,*args):
        pass


