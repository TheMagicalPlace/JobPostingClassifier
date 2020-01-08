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

class NBDatum:

    def __init__(self,data : str,label : str):
        self.data : str = data
        self.label : str  = label
        self.sent_tokens : List[str] = None
        self.word_tokens : List[str] = None


class NBdataset:

    def __init__(self,encoded_data: List[List],encoded_labels : List[List]):
        self.content = []
        self.label = []
        self.encoded_data = encoded_data
        self.encoded_labels = encoded_labels


class PrepareDataHash:
    def __init__(self,filepaths : List[str] = None):
        self.filepaths = filepaths
        self.jobs = []
        self.paths = []
        self.jobdesc_preprocessing()
        self.dataset = NBdataset([],[])
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
                self.jobs.append(NBDatum(job.path,'Bad'))
                self.paths.append(job.path)
        for nums, job in enumerate(jobs_good):
            with open(f'Good_Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(job.path,'Good'))
        for num, job in enumerate(jobs_okay):
            with open(f'Neutral Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(job.path,'Neutral'))
        for num, job in enumerate(jobs_good):
            with open(f'Ideal Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(job.path,'Ideal'))



class PrepareNBdata:

    def __init__(self,filepaths : List[str] = None):
        self.filepaths = filepaths
        self.jobs = []
        self.goodjobs_encoded = {}
        self.badjobs_encoded = {}
        self.dataset = NBdataset([],[])

    def jobdesc_preprocessing(self):
        '''Creating the objects containing the label and content'''
        jobs_bad = os.scandir('Bad Jobs/')
        jobs_good = os.scandir('Good_Jobs/')
        jobs_okay = os.scandir('Neutral Jobs/')
        jobs_ideal = os.scandir('Ideal Jobs/')
        for num,job in enumerate(jobs_bad):
            with open(f'Bad Jobs/{job.name}','r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Bad'))
                self.dataset.content.append(jobdesc.read())
                self.dataset.label.append('Bad')
        for nums, job in enumerate(jobs_good):
            with open(f'Good_Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Good'))
                self.dataset.content.append(jobdesc.read())
                self.dataset.label.append('Good')
        for num, job in enumerate(jobs_okay):
            with open(f'Neutral Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Neutral'))
                self.dataset.content.append(jobdesc.read())
                self.dataset.label.append('Neutral')
        for num, job in enumerate(jobs_ideal):
            with open(f'Ideal Jobs/{job.name}', 'r') as jobdesc:
                self.jobs.append(NBDatum(jobdesc.read(),'Good'))
                self.dataset.content.append(jobdesc.read())
                self.dataset.label.append('Good')

    def create_tokens_alt(self):
        raw = []
        lab = []
        for obj in self.jobs:
            raw.append(obj.data)
            lab.append(obj.label)

        X_train, X_test, y_train, y_test = train_test_split(raw, lab,
                                                            test_size=0.4)


        vectorizer = HashingVectorizer(analyzer = 'word',stop_words='english', alternate_sign=False)

        X_train = vectorizer.fit_transform(X_train)
        X_test = vectorizer.fit_transform(X_test)

        ch2 = SelectKBest(chi2, k=15)

        X_train = ch2.fit_transform(X_train,y_train)
        X_test = ch2.fit_transform(X_test,y_test)


        bench = BenchmarkSuite(X_train=X_train,y_test=y_test,X_test=X_test,y_train=y_train)
        bench.show_results()


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

    def process_to_NB_compatible(self):
        count_vect = CountVectorizer()
        raw = []
        r2 = []
        for job in self.jobs:
            raw.append(" ".join(job.word_tokens))
            r2 += job.word_tokens
        count = count_vect.fit_transform(raw)
        transformer = TfidfTransformer().fit(count)
        count = transformer.transform(count)
        self.count = count



    def create_dataset(self):
        self.jobdesc_preprocessing()
        self.create_tokens_alt()
        #self.process_to_NB_compatible()

        #labelenc = list([dat.label for dat in self.jobs])
        #return NBdataset(self.count,labelenc)
        #return NBdataset(dataenc,labelenc)

class MLClassifyRWData:
    pass


if __name__ == '__main__':
    NBdata = PrepareNBdata()
    NBdata.create_dataset()
    daat2 = PrepareDataHash()

if __name__ == '__main__s':
    iris = datasets.load_iris()
    NBdata = PrepareNBdata()
    daat2 = PrepareDataHash()
    dataset = NBdata.create_dataset()
    xx,yy,yyy,yyyy = [],[],[],[]
    for i in range(30,90):
        X_train, X_test, y_train, y_test = train_test_split(dataset.encoded_data, dataset.encoded_labels, test_size=i/100)
        model1 = ComplementNB(norm=True).fit(X_train,y_train)
        model2 =svm.SVC(gamma='auto',probability=True).fit(X_train,y_train)
        model3 =MultinomialNB().fit(X_train,y_train)
        predicted1 = model1.predict(X_test)
        predicted2 = model2.predict(X_test)
        predicted3 = model3.predict(X_test)
        xx.append(i/100)
        score1 = metrics.accuracy_score(y_test,predicted1)
        score2 = metrics.accuracy_score(y_test, predicted2)
        score3 = metrics.accuracy_score(y_test, predicted3)
        pre1 =metrics.classification_report(y_test,predicted1,labels=[1,0,-1])
        yy.append(np.mean(predicted1 == y_test))
        yyy.append(np.mean(predicted2 == y_test))
        yyyy.append(np.mean(predicted3 == y_test))

    print(np.mean(yy),std(yy),'\n',np.mean(yyy),std(yyy),'\n',np.mean(yyyy),std(yyyy))
    plt.plot(xx,yy)
    plt.plot(xx,yyy)
    plt.plot(xx,yyyy)
    plt.legend(['Complement NB','Support Vector Machinery','Multinomial NB'])
    plt.show()












