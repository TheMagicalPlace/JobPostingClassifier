









#TODO fix file extension stuff for windows compatibility
#TODO check out why occasional hangs on 1st job page

import time
import re
import abc
from datetime import timedelta
import json
import os
from typing import Iterable
class ScraperBase(abc.ABC):
    """Abstract base class for all of my job board web scrapers"""


    time_ago_re = re.compile(r"([0-9]+)[+]?( days? ago)")

    def __init__(self,driver,save_every=10,file_path_args : Iterable[str] = ()):
        self.driver = driver
        self.job_dict = {}     # Holds each job posting
        self.calls = 0         # calls made to the scraper
        self.fpargs = file_path_args
        self.save_every = save_every
        try:
            os.makedirs(os.path.join(os.getcwd(),*file_path_args))
        except FileExistsError:
            pass


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

    def save_data_json(self):
        print(os.path.join(os.getcwd(),self.fpargs,"jobs_data.json"))
        jpath = os.path.join(os.getcwd(),self.fpargs,"jobs_data.json")
        if os.path.exists(jpath):
            with open(os.path.join(os.getcwd(),self.fpargs,"jobs_data.json"),'r+') as jobdat:
                print(self.fpargs)
                self.job_dict.update(json.loads(jobdat.read()))
                jobdat.write(json.dumps(self.job_dict))
        else:
            with open(os.path.join(os.getcwd(),self.fpargs,"job_data.json"),'w') as jobdat:
                jobdat.write(json.dumps(self.job_dict))

    def scrape_page(self, element):
        """
        scrapes single job page after the driver loads a new job posting.
        Returns data as a dictionary
        """

        # wait ~1 second for elements to be dynamically rendered
        time.sleep(0.2)
        start = time.time()
        self.calls+=1

        post_date=self.format_time(self.get_post_date(element))
        job_info = {
            "link"             : self.get_link(element),
            "job_name"         : self.get_job_name(element),
            "company"          : self.get_company_name(element),
            "location"         : self.get_job_location(element),
            "description"      : self.get_description(element),
            'date_posted'      : post_date,
            'age'              : post_date if not isinstance(post_date,time.struct_time)
                                           else timedelta(time.time(),self.format_time(self.get_post_date(element)))
        }

        job_uid = job_info['job_name']+job_info['company']
        self.job_dict[job_uid] = job_info

        # saves every i calls to prevent data loss if the webdriver runs into an issue
        if not self.calls % self.save_every:
            self.save_data_json()



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


