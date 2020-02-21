import os
from itertools import chain
from collections import Counter
import random
from copy import deepcopy
import numpy as np
from matplotlib import pyplot as plt
from typing import List,AnyStr
from sklearn import datasets,preprocessing
from sklearn.naive_bayes import MultinomialNB,ComplementNB,BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from numpy import std
from sklearn import svm

from benchmarks import *

from sklearn.feature_extraction.text import HashingVectorizer
import nltk.data
from nltk.tokenize import word_tokenize,sent_tokenize,mwe
from nltk.stem import PorterStemmer

from collections import defaultdict

class PrepareNBdata:

    job_label_associations = {'Good Jobs':'Good', 'Bad Jobs':'Bad', 'Neutral Jobs':'Neutral', 'Ideal Jobs':'Ideal'}

    def __init__(self,search_term : List[str]):
        self.search_term = search_term
        self.jobs = []
        self.goodjobs_encoded = {}
        self.badjobs_encoded = {}
        self.dataset = defaultdict(list)

    def jobdesc_preprocessing(self):
        '''Creating the objects containing the label and content'''

        paths = {}
        job_cat_data = {}
        for subfolder in ['Good Jobs', 'Bad Jobs', 'Neutral Jobs', 'Ideal Jobs']:
            paths[subfolder] = os.path.join(os.getcwd(), self.search_term, 'Train', subfolder)
            job_cat_data[subfolder] = os.scandir(os.path.join(os.getcwd(), self.search_term, 'Train', subfolder))
        for joblabel,data in job_cat_data.items():
            for job in data:
                with open(os.path.join(paths[joblabel],job.name), 'r') as jobdesc:
                    self.dataset['content'].append(jobdesc.read())
                    self.dataset['label'].append(PrepareNBdata.job_label_associations[joblabel])


    def live_job_processing(self,directory):

        with open(directory,'r') as job:
            content = [job.read()]
        content = self.vectorizer.transform(content)
        content = self.ch2.transform(content)
        label = self.rf_classify.predict(content)
        return label

    def format_raw_text(self):


        X_train, X_test, y_train, y_test = train_test_split(self.dataset['content'], self.dataset['label'],test_size=0.8)

        self.vectorizer = HashingVectorizer(analyzer = 'word',stop_words='english', alternate_sign=False)
        self.ch2 = SelectKBest(chi2, k=15)

        #vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,stop_words='english')

        X_train = self.vectorizer.transform(X_train)
        X_test = self.vectorizer.transform(X_test)

        self.X_train = self.ch2.fit_transform(X_train,y_train)
        self.X_test = self.ch2.transform(X_test)
        self.y_train,self.y_test = y_train,y_test

    def create_tokens(self):
        common_words = ['·',',','.','to','the','and','of','or','with','in','you','your','(',')',':',' a ','/','is']
        label_converter = {'Ideal' :1,'Good' : 1 , 'Neutral' : 1,'Bad':-1}
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        stemmer = PorterStemmer()
        #self.randomselect = random.sample(self.jobs,len(self.jobs)//3)


        for job in self.jobs:
            job.label = label_converter[job.label]
            job.sent_tokens = sent_detector.tokenize(job.data.strip())
            jobwordform = job.data.replace('[^\w\s]', '').lower()
            for common in common_words:
                jobwordform = jobwordform.replace(common,' ')
            wordtokens = word_tokenize(jobwordform)
            c = Counter(wordtokens)
            job.word_tokens = [stemmer.stem(wordtoken) for wordtoken in wordtokens]

    def model_data(self):
        self.jobdesc_preprocessing()
        self.format_raw_text()
        bench = BenchmarkSuite(X_train=self.X_train,y_test=self.y_test,X_test=self.X_test,y_train=self.y_train)
        self.rf_classify = bench.random_forest()
        print('')



if __name__ == '__main__':
    search = PrepareNBdata('Chemical Engineer')
    search.model_data()










