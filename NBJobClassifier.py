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
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from numpy import std
from sklearn import svm


import nltk.data
from nltk.tokenize import word_tokenize,sent_tokenize,mwe
from nltk.stem import PorterStemmer

class NBDatum:

    def __init__(self,data : str,label : str):
        self.data : str = data
        self.label : str  = label
        self.sent_tokens : List[str] = None
        self.word_tokens : List[str] = None


class NBdataset:

    def __init__(self,encoded_data: List[List],encoded_labels : List[List]):
        self.encoded_data = encoded_data
        self.encoded_labels = encoded_labels


class PrepareNBdata:

    def __init__(self,filepaths : List[str] = None):
        self.filepaths = filepaths
        self.jobs = []
        self.goodjobs_encoded = {}
        self.badjobs_encoded = {}

    def jobdesc_preprocessing(self):
        '''Creating the objects containing the label and content'''
        jobs_bad = os.scandir('Bad Jobs/')
        jobs_good = os.scandir('Good_Jobs/')
        jobs_okay = os.scandir('Neutral Jobs/')
        jobs_ideal = os.scandir('Ideal Jobs/')
        for num,job in enumerate(jobs_bad):
            with open(f'Bad Jobs/{job.name}','r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Bad'))
        for nums, job in enumerate(jobs_good):
            with open(f'Good_Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Good'))
        for num, job in enumerate(jobs_okay):
            with open(f'Neutral Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Neutral'))
        for num, job in enumerate(jobs_good):
            with open(f'Ideal Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Ideal'))

    def create_tokens(self):
        common_words = ['·',',','.','to','the','and','of','or','with','in','you','your','(',')',':',' a ','/','is']
        label_converter = {'Ideal' :2,'Good' : 1 , 'Neutral' : 0,'Bad':-1}
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        stemmer = PorterStemmer()
        self.randomselect = random.sample(self.jobs,len(self.jobs)//3)


        for job in self.randomselect:
            job.label = label_converter[job.label]
            job.sent_tokens = sent_detector.tokenize(job.data.strip())
            jobwordform = job.data.replace('[^\w\s]', '').lower()
            #for common in common_words:
            #    jobwordform = jobwordform.replace(common,'')
            wordtokens = word_tokenize(jobwordform)
            c = Counter(wordtokens)
            job.word_tokens = [stemmer.stem(wordtoken) for wordtoken in wordtokens]

    def process_to_NB_compatible(self):
        count_vect = CountVectorizer()
        raw = []
        r2 = []
        for job in self.randomselect:
            raw.append(" ".join(job.word_tokens))
            r2 += job.word_tokens
        count = count_vect.fit_transform(raw)
        transformer = TfidfTransformer().fit(count)
        count = transformer.transform(count)
        self.count = count



    def create_dataset(self):
        self.jobdesc_preprocessing()
        self.create_tokens()
        self.process_to_NB_compatible()

        labelenc = list([dat.label for dat in self.randomselect])
        return NBdataset(self.count,labelenc)
        #return NBdataset(dataenc,labelenc)




if __name__ == '__main__':
    iris = datasets.load_iris()
    NBdata = PrepareNBdata()
    dataset = NBdata.create_dataset()
    xx,yy,yyy,yyyy = [],[],[],[]
    for i in range(5,81):
        X_train, X_test, y_train, y_test = train_test_split(dataset.encoded_data, dataset.encoded_labels, test_size=i/100)
        model1 = ComplementNB().fit(X_train,y_train)
        model2 =svm.SVC(gamma='auto').fit(X_train,y_train)
        model3 =MultinomialNB().fit(X_train,y_train)
        predicted1 = model1.predict(X_test)
        predicted2 = model2.predict(X_test)
        predicted3 = model3.predict(X_test)
        xx.append(i/100)
        yy.append(np.mean(predicted1 == y_test))
        yyy.append(np.mean(predicted2 == y_test))
        yyyy.append(np.mean(predicted3 == y_test))

    print(np.mean(yy),std(yy),'\n',np.mean(yyy),std(yyy),'\n',np.mean(yyyy),std(yyyy))
    plt.plot(xx,yy)
    plt.plot(xx,yyy)
    plt.plot(xx,yyyy)
    plt.legend(['Complement NB','Support Vector Machinery','Multinomial NB'])
    plt.show()












