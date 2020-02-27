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

from utils import *


from tqdm import tqdm
from nltk import word_tokenize
from pymagnitude import *


from collections import defaultdict

from SK_learn_pipelines import *
from NLTKUtils import *

glove = Magnitude("./vectors/glove.6B.100d.magnitude")
def avg_glove(df):
    vectors = []
    for title in df.content.values:
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
                    for _ in range(3):
                        print(jobdesc.readline())
                    self.dataset['content'].append(jobdesc.read())
                    self.dataset['label'].append(PrepareNBdata.job_label_associations[joblabel])
        self.dataset = pd.DataFrame(self.dataset)
        print(self.dataset)

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




    def format_raw_text(self):

        common_words = ['·', ',', '.', 'to', 'the', 'and', 'of', 'or', 'with', 'in', 'you', 'your', '(', ')', ':',
                        ' a ', '/', 'is']


        train,test = train_test_split(self.dataset,test_size=0.2,stratify = self.dataset.label,shuffle=True)



        y_train,y_test = train.label,test.label
        #y_train = np.where(train.label.values == 'Good', 1, 0)
        #y_test = np.where(test.label.values == 'Good', 1, 0)

        self.vectorizer = CountVectorizer()
        self.ch2 = SelectKBest(chi2, k=50)

        X_train = self.vectorizer.fit_transform(train.content.values)
        X_test = self.vectorizer.transform(test.content.values)

        run_log_reg(X_train, X_test, y_train, y_test)

        self.vectorizer = TfidfVectorizer()
        X_train = self.vectorizer.fit_transform(train.content.values)
        X_test = self.vectorizer.transform(test.content.values)

        run_log_reg(X_train, X_test, y_train, y_test)

        X_train = avg_glove(train)
        X_test = avg_glove(test)

        run_log_reg(X_train, X_test, y_train, y_test)

        tfidf = TfidfVectorizer()
        tfidf.fit(train.content.values)
        idf_dict = dict(zip(tfidf.get_feature_names(), tfidf.idf_))

        X_train = tfidf_glove(train,idf_dict)
        X_test = tfidf_glove(test,idf_dict)

        run_log_reg(X_train, X_test, y_train, y_test)



        MODEL_PATH = './encoder/infersent1.pkl'
        params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048, 'pool_type': 'max', 'dpout_model': 0.0,
                        'version': 1}

        infersent = InferSent(params_model)
        infersent.load_state_dict(torch.load(MODEL_PATH))

        infersent.set_w2v_path('GloVe/glove.840B.300d.txt')
        infersent.build_vocab(train.content.values, tokenize=False)

        x_train = infersent.encode(train.content.values, tokenize=False)
        x_test = infersent.encode(test.content.values, tokenize=False)
        run_log_reg(x_train, x_test, y_train, y_test, alpha=1e-4)





        self.X_train,self.X_test = X_train,X_test
        self.y_train,self.y_test = y_train,y_test




    def model_data(self):
        self.jobdesc_preprocessing()
        self.format_raw_text()

        ##bench.show_results()
        #self.rf_classify = bench.random_forest()
        #print('')



if __name__ == '__main__':
    search = PrepareNBdata('Chemical Engineer')
    search.model_data()










