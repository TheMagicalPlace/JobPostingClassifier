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
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
import pandas as pd
from benchmarks import *
import annoy
from sklearn.utils import shuffle
from Infersent.models import InferSent
import torch
import shutil
from utils import *
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer,WordNetLemmatizer
from sklearn import svm
from sklearn import datasets
from tqdm import tqdm
from nltk import word_tokenize
from pymagnitude import *

import re
from collections import defaultdict

from SK_learn_pipelines import *
from NLTKUtils import *
from featurization import *
glove = Magnitude("./vectors/glove.6B.100d.magnitude")

def dummy(doc):
    return doc


def avg_glove(df):
    vectors = []
    for title in tqdm(df.content.values):
        vectors.append(np.average(glove.query(word_tokenize(title)), axis = 0))
    return np.array(vectors)

def tfidf_glove(df,idf_dict):
    vectors = []
    for title in tqdm(df.content.values):
        glove_vectors = glove.query(word_tokenize(title))
        weights = [idf_dict.get(word, 1) for word in word_tokenize(title)]
        vectors.append(np.average(glove_vectors, axis = 0, weights = weights))
    return np.array(vectors)

class PrepareNBdata:

    job_label_associations = {'Good Jobs':1, 'Bad Jobs':0, 'Neutral Jobs':0, 'Ideal Jobs':1}

    def __init__(self,search_term : str):
        self.search_term = search_term
        self.jobs = []
        self.goodjobs_encoded = {}
        self.badjobs_encoded = {}
        self.dataset = defaultdict(list)
        self._jobdesc_preprocessing()

    def _process_text(self):
        pass
    def _jobdesc_preprocessing(self):
        '''Processes the text files to remove punctuation, noise (i.e url's), and case from the text
         and assignes the result to a pandas dataframe containing the label and content'''

        paths = {}
        lemma = LemmaTokenizer()
        snowball_stemmer = SnowballTokenizer()
        job_cat_data = {}
        for subfolder in ['Good Jobs', 'Bad Jobs', 'Neutral Jobs', 'Ideal Jobs']:
            paths[subfolder] = os.path.join(os.getcwd(), self.search_term, 'Train', subfolder)
            job_cat_data[subfolder] = os.scandir(os.path.join(os.getcwd(), self.search_term, 'Train', subfolder))
        for joblabel,data in job_cat_data.items():
            for job in data:
                with open(os.path.join(paths[joblabel],job.name), 'r') as jobdesc:
                    raw = jobdesc.readlines()[7:]
                    raw = " ".join(raw)
                    raw = snowball_stemmer(raw)
                    #raw = snowball_stemmer(" ".join(raw))


                formatted_data = raw
                self.dataset['content'].append(formatted_data)
                self.dataset['label'].append(PrepareNBdata.job_label_associations[joblabel])
        self.dataset = pd.DataFrame(self.dataset)


    def live_job_processing(self,directory):

        with open(directory,'r') as job:
            content = [job.read()]
        content = self.vectorizer.transform(content)
        content = self.ch2.transform(content)
        label = self.rf_classify.predict(content)
        return label

    def text_processing(self):

        X_train, X_test, y_train, y_test = train_test_split(self.dataset['content'], self.dataset['label'],
                                                            test_size=0.5)




    def vectorize_text(self,Training=True):
        if Training:
            train,test = train_test_split(self.dataset,test_size=0.3,stratify = self.dataset.label,shuffle=True)

            y_train,y_test = train.label,test.label
            self.vectorizer = CountVectorizer(tokenizer=dummy,preprocessor=dummy)
            self.transformer = TfidfTransformer()





            X_train = self.vectorizer.fit_transform(train.content.values)
            X_test = self.vectorizer.transform(test.content.values)
            self.transformer.fit(X_train, y_train)
            #X_train = self.transformer.transform(X_train)
            #X_test = self.transformer.transform(X_test)

            self.X_train,self.X_test = X_train,X_test
            self.y_train,self.y_test = y_train,y_test

        else:
            self.live_vectorizer = TfidfVectorizer(analyzer='word', stop_words='english').fit(self.dataset.content)

    def model_data(self):
        self.vectorize_text()
        bench = BenchmarkSuite(self.X_train,self.X_test,self.y_train,self.y_test)
        bench.show_results(silent=True,plot=False)
        #self.rf_classify = bench.random_forest()
        #print('')



if __name__ == '__main__':
    old = []
    try:
        with open(os.path.join(os.getcwd(), 'Models', 'model_stats.json'), 'r') as models:
            last = json.loads(models.read())
        os.unlink(os.path.join(os.getcwd(), 'Models', 'model_stats.json'))
    except FileNotFoundError:
        last = defaultdict(int)
    for i in range(5,0,-1):
        try:
            with open(os.path.join(os.getcwd(), 'Models','Testing', f'model_stats_{i}.json'), 'r') as models:
                old.append(json.loads(models.read()))
        except FileNotFoundError:
            with open(os.path.join(os.getcwd(), 'Models','Testing', f'model_stats_{i}.json'), 'w') as models:
                models.write(json.dumps(last))
            old.append(last)
            break
    else:
        for i in range(1,5):
            if i == 1:
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i}.json'), 'r') as models:
                    holder = json.loads(models.read())
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i}.json'), 'w') as models:
                    models.write(json.dumps(last))
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i+1}.json'), 'r') as models:
                    holder2 = json.loads(models.read())
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i+1}.json'), 'w') as models:
                    models.write(json.dumps(holder))
            else:
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i+1}.json'), 'r') as models:
                    holder2 = json.loads(models.read())
                with open(os.path.join(os.getcwd(), 'Models', 'Testing', f'model_stats_{i+1}.json'), 'w') as models:
                    models.write(json.dumps(holder))
            holder = holder2


    search = PrepareNBdata('Chemical Engineer')
    for _ in range(10):

        search.model_data()
    with open(os.path.join(os.getcwd(), 'Models', 'model_stats.json'), 'r') as models:
        models = json.loads(models.read())


    clf = [k for k in models.keys()]
    formatted = defaultdict(list)
    maxl = max([len(mod) for mod in clf])
    for mod in clf:
        for i in range(0, 5):
            if i+1 > len(old):
                break
            else:
                formatted[mod].append(old[i][mod])
    labels = ['Model','| Last ',1,2,3,4,5]
    labels[0] = labels[0].center(maxl)
    for i,l in enumerate(labels[2:]):
        labels[i+2] = f'|   {labels[i+2]}  '
    print("".join(labels))
    print('-'*len("".join(labels)))
    for mod in clf:
        str = f'{mod}'
        str = str.ljust(maxl)
        str += f'| {models[mod]:.2f} '
        for _ in formatted[mod][::-1]:
            str += f'| {_:.2f} '
        print(str)










