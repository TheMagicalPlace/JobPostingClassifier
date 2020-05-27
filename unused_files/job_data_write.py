import json
import os
import re

class JSONProcessor:
    """ Turns job data containing JSON file into text document for each individual job"""
    def __init__(self,search_term):
        try:
            with open(os.path.join(os.getcwd(),search_term,'job_link_file'),'r') as jobs:
                self.joblinks = json.loads(jobs.read())
        except FileNotFoundError:
            self.joblinks = {}
        finally:
            self.search_term = search_term


    def __call__(self):

        # jobs that have already been processed are skipped
        extant_jobs = [job.name for job in os.scandir(os.path.join(self.search_term,'Train','Good Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Train','Bad Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Train','Ideal Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Train','Neutral Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Train','Other'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Results','Good Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Results','Bad Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Results','Ideal Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Results','Neutral Jobs'))] + \
                      [job.name for job in os.scandir(os.path.join(self.search_term,'Unsorted'))]


        with open(os.path.join(os.getcwd(),self.search_term,'jobs_data'),'r') as data:
            jobdat = json.loads(data.read())

        for key,info in jobdat.items():
            key = re.sub('/',' ',key)
            if key in extant_jobs:
                continue

            # writing new job to a text file
            with open(os.path.join(os.getcwd(),self.search_term,'Unsorted',key),'w') as jobfile:
                self.joblinks[info['link']] = os.path.join(os.getcwd(), self.search_term,'Unsorted', key)
                for _,infodat in info.items():
                    try:
                        jobfile.write(infodat)
                        jobfile.write('\n\n')
                    except TypeError:
                        continue
        # creating a file containing the link to each job
        with open(os.path.join(os.getcwd(),self.search_term,'job_link_file'),'w') as job:
            d = json.dumps(self.joblinks)
            job.write(d)

    def modify_json_file(self):
        with open(os.path.join(os.getcwd(),self.search_term,'job_link_file'),'w') as job:
            d = json.dumps(self.joblinks)
            job.write(d)



if __name__ == '__main__':
    json_to_text = JSONProcessor('Chemical Engineer')
    json_to_text()
    print(len([e for e in os.scandir('../Chemical Engineer/')]))