from ScraperIndeed import *
from job_data_write import *
from file_tree_setup import *
from NBJobClassifier import *
import json
import os
from  collections import defaultdict

class SearchHandler:

    # seperate from the one used in the classification handler to prevent inappropriate file assignment
    job_label_associations = {'Good Jobs': 'Good', 'Bad Jobs': 'Bad', 'Neutral Jobs': 'Neutral', 'Ideal Jobs': 'Ideal'}
    label_to_job_cat = {v:k for k,v in job_label_associations.items()}

    def __init__(self,search_term,results_to_find,equivlant_to = None):
        """Sets up file structure if needed and assigns instance variables, creates scraper object"""
        if equivlant_to is not None:
            self.search_term = search_term
            self.file_term = equivlant_to
        else:
            self.search_term = search_term
            self.file_term = search_term

        file_setup(self.file_term)
        self.scraper = IndeedClient(search_term,self.file_term)

        self.no_of_results = results_to_find
        self.results = defaultdict(list)

    def __call__(self, *args, **kwargs):
        """Scrapes and classifies job data based on setup data"""

        self.classifier = ClassificationHandler(self.file_term,training=False)
        self.scraper(jobs_to_find=self.no_of_results)
        self.json_reader = JSONProcessor(self.file_term)
        self.json_reader()
        self.classify()

    def get_data(self):
        """Scrapes and converts jobs to text docs. without doing any further sorting"""
        self.scraper(jobs_to_find=self.no_of_results)
        self.json_reader()

    def classify(self):
        """ Classifies all unsorted files"""
        with open(os.path.join(os.getcwd(),self.file_term,'job_link_file'),'r') as links:
            lnks = json.loads(links.read())
        for link,file_path in lnks.items():
            end = os.path.basename(file_path)

            # assign label
            label = self.classifier.live_job_processing(file_path)[0]
            self.results[label].append(link)

            # move file from 'unsorted' to result corresponding to label
            os.replace(file_path,os.path.join(os.getcwd(),self.file_term,'Results',self.label_to_job_cat[label],end))
            with open(os.path.join(os.getcwd(),self.file_term,'Results',self.label_to_job_cat[label],'links'),'a') as links:
                links.write(link)
                links.write('\n\n\n')

            # removes sorted jobs from json link file
            del self.json_reader.joblinks[link]
            self.json_reader.modify_json_file()


if __name__ == '__main__':
    a = True
    results = 50
    term = 'Entry Level Software Engineer'
    search = SearchHandler(term, results,equivlant_to='Entry Level Computer Programmer')
    if a:
        search()
    else:
        search.get_data()