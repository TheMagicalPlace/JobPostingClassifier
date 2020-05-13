import os
import sqlite3
from ui import file_tree_setup


class util:
    file_term = "../Chemical Engineer"
    def _jobdesc_preprocessing(self):
        '''Processes the text files to remove punctuation, noise (i.e url's), and case from the text
         and assignes the result to a pandas dataframe containing the label and content'''
        file_tree_setup.file_setup(self.file_term)
        self.database = sqlite3.connect(os.path.join(os.getcwd(), self.file_term, f'{self.file_term}.db'))
        job_cat_data = {}
        paths = {}
        with self.database:
            cur = self.database.cursor()
            for subfolder in ['Good Jobs', 'Bad Jobs', 'Neutral Jobs', 'Ideal Jobs']:
                paths[subfolder] = os.path.join(os.getcwd(), self.file_term, 'Train', subfolder)
                job_cat_data[subfolder] = os.scandir(os.path.join(os.getcwd(), self.file_term, 'Train', subfolder))
            for joblabel, data in job_cat_data.items():
                for job in data:
                    with open(os.path.join(paths[joblabel], job.name), 'r') as jobdesc:
                        raw = jobdesc.readlines()[7:]
                        formatted_data = " ".join(raw)
                        name = job.name.split('-')[0]
                        cur.execute("INSERT INTO training VALUES (?,?,?,?)",
                                    (job.name, joblabel,name,formatted_data))


u = util()
u._jobdesc_preprocessing()