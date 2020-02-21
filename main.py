from ScraperIndeed import *
from job_data_write import *
from file_tree_setup import *
from NBJobClassifier import *
import json
import os


class SearchHandler:
    def __init__(self,search_term,results_to_find):
        self.search_term = search_term
        file_setup(search_term)
        self.scraper = IndeedClient(search_term)
        self.no_of_results = results_to_find
        classifier = PrepareNBdata()
    def __call__(self, *args, **kwargs):
        self.scraper(results_to_find)



    def classify(self):
        with open(os.path.join(os.getcwd(),self.search_term,'job_link_file'),'r') as links:
            lnks = json.loads(links.read())


scraper_obj = IndeedClient()
scraper_obj('Chemical Engineer',200)

