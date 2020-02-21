from ScraperIndeed import *
from job_data_write import *
from file_tree_setup import *
from NBJobClassifier import *
import json
import os
from  collections import defaultdict

class SearchHandler:
    label_to_job_cat = {v:k for k,v in PrepareNBdata.job_label_associations.items()}

    def __init__(self,search_term,results_to_find):
        self.search_term = search_term
        file_setup(search_term)
        self.json_reader = JSONProcessor(search_term)
        self.scraper = IndeedClient(search_term)
        self.no_of_results = results_to_find
        self.results = defaultdict(list)
    def __call__(self, *args, **kwargs):
        self.classifier = PrepareNBdata(self.search_term)
        self.classifier.model_data()
        self.scraper(jobs_to_find=self.no_of_results)
        self.json_reader()
        self.classify()
    def get_data(self):
        self.scraper(jobs_to_find=self.no_of_results)
        self.json_reader()

    def classify(self):

        with open(os.path.join(os.getcwd(),self.search_term,'job_link_file'),'r') as links:
            lnks = json.loads(links.read())
        for link,file_path in lnks.items():
            end = os.path.basename(file_path)
            label = self.classifier.live_job_processing(file_path)[0]
            self.results[label].append(link)
            os.replace(file_path,os.path.join(os.getcwd(),self.search_term,'Results',self.label_to_job_cat[label],end))
            with open(os.path.join(os.getcwd(),self.search_term,'Results',self.label_to_job_cat[label],'links'),'a') as links:
                links.write(link)
                links.write('\n\n\n')
            del self.json_reader.joblinks[link]
            self.json_reader.modify_json_file()


if __name__ == '__main__':
    a = False
    results = 50
    term = 'Entry Level Computer Programmer'
    search = SearchHandler(term, results)
    if a:
        search()
    else:
        search.get_data()