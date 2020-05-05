import os
from typing import Any, Iterable

from joblib import dump
from numpy import product
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import PassiveAggressiveClassifier, LogisticRegression, LogisticRegressionCV
from sklearn.linear_model import Perceptron
from sklearn.linear_model import RidgeClassifierCV
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, Normalizer, RobustScaler
from sklearn.svm import LinearSVC, SVC

from sklearn_tools.sklearn_extensions.NLTKUtils import *


def _():
    duals = [True, False]
    penaltys = ['l1', 'l2']
    losses = ['hinge', 'squared_hinge']
    all_params = list(product(duals, penaltys, losses))
    return all_params
def dummy(doc):
    return doc


def svc_compatability_handler(model,dual : bool):
    if dual:
        if model == "LinearSVC":
            params = {
            'penalty': ['l2'],
            'loss': ['hinge', 'squared_hinge'],
            'C': [0.01,0.1, 1, 10],
            'tol': [1e-2, 1e-3, 1e-4],
            'fit_intercept': [True],
            'max_iter': [-1],  # [100, 1000, 2500],
            'dual': [True]}
    else:
        if model == "LinearSVC":
            params = {
            'penalty': ['l2'],
            'loss': ['squared_hinge'],
            'C': [0.01,0.1, 1, 10,],
            'tol': [1e-2, 1e-3, 1e-4],
            'fit_intercept': [True],
            'max_iter': [-1],  # [100, 1000, 2500],
            'dual': [False]}
    return params
class ModelTuningParams:



    models= {
        'Perceptron': {
            'penalty': ['l2' ,'l1',],
            'max_iter' : [5000],
            'tol' : [1e-2,1e-3,1e-4],
            'shuffle' : [True,False],
            'eta0' : [0.1,1,10],
            'n_jobs' : [-1],
            'n_iter_no_change' : [5,25,100],
            'early_stopping' : [False,True]
        },
        'RidgeClassifierCV': {
            'alpha' : [0.1,1,10,100,1000],
            'fit_intercept' : [True,False],
            'max_iter': [-1],#[100, 1000, 5000],
            'tol': [1e-2, 1e-3, 1e-4],
            'solver' : ['auto', 'sparse_cg', 'sag'],
        },
        'PassiveAggressiveClassifier':{
            'C': [0.1, 1, 10, 100],
            'max_iter':[-1],# [100, 1000, 5000],
            'tol': [1e-2, 1e-3, 1e-4],
            'early_stopping': [False, True],
            'fit_intercept' : [False,True],
            'loss' : ['hinge','square_hinge'],
            'n_jobs' : [-1],
            'shuffle' : [True]
        },
        'KNeighborsClassifier' : {
            'n_neighbors' : [5,25,50],
            'algorithm' : ['auto','ball_tree','kd_tree'],
            'leaf_size' : [10,30,80,125],
            'n_jobs': [-1],
        },
        'RandomForestClassifier' : {
            'n_estimators' : [10,100,500,1000],
            'criterion' : ['gini'],
            'max_depth' : [None],
            'min_samples_split' : [2],
            'min_samples_leaf' : [1],
            'min_weight_fraction_leaf' : [0.],
            'min_impurity_decrease' : [0.],
            'bootstrap' : [True],
            'oob_score' : [False],
            'random_state': [42],
            'max_features' : ['auto','log2',10,500,None],
            'max_leaf_nodes' : [10,50,100,None],
            'n_jobs' : [-1]
        },

        'LogisticRegressionCV': {
            'penalty': ['l2',], #'elasticnet'],
            'max_iter' : [5000],
            'Cs': [0.01,0.1, 1, 10],
            'tol': [1e-2, 1e-3, 1e-4],
            'fit_intercept': [False, True],
            'solver': ['lbfgs',], # 'sag', 'saga','lbfgs',],
            'dual': [False]},

        'LogisticRegression': {
            'penalty': ['l2',], # 'elasticnet'],
            'max_iter': [5000],
            'C': [0.01, 0.1, 1, 10, 100],
            'tol': [0.1,1e-2, 1e-3, 1e-4],
            'fit_intercept': [False, True],
            'solver': ['lbfgs',], #, 'sag', 'saga','lbfgs',],
            'dual': [False]},

        'LinearSVC':              {
            'penalty': ['l2'],
            'loss': ['squared_hinge'],
            'C': [0.01,0.1, 1, 10,],
            'tol': [1e-2, 1e-3, 1e-4],
            'fit_intercept': [True],
            'max_iter': [5000,10000],  # [100, 1000, 2500],
            'dual': [False]},
        'SVC' : {
            'C': [0.1, 1, 10, 100, 1000],
            'kernel' : ['rbf','poly','sigmoid'],
            'gamma' : ['scale','auto',0.1,1,10],
            'coef0' : [0,0.1,1,10],
            'tol': [1e-2, 1e-3, 1e-4],
            'max_iter': [-1], #[100, 1000, 5000,-1],


        },
        'SGDClassifier' : {
            #'alpha': [0.0001,0.001,0.1, 1, 10, 100, 1000],
            'penalty': ['l1', 'l2',"elasticnet"],
            'loss': ['hinge','modified_huber'],
            #'l1_ratio' : [0.05,0.15,0.3,0.5],
            #'fit_intercept': [True],
            'max_iter': [2500,5000],
            #'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'shuffle' : [False],
            'epsilon' : [0.1,0.5,1],
            'learning_rate' : ['optimal','adaptive'],
            'eta0': [0.00001, 1],
            'early_stopping': [True],
            #'power_t' : [0.5]
        },
        'MultinomialNB' : {
            'alpha' : [0.1,1,10,100],
            'fit_prior' : [True,False]
        },
        'BernoulliNB': {
            'alpha': [0.1, 1, 10, 100],
            'fit_prior': [True, False]
        },
        'ComplimentNB': {
            'alpha': [0.1, 1, 10, 100],
            'fit_prior': [True, False],
            'norm' : [True,False]
        }
    }



class PipelineComponents:
    models = {
        'RidgeClassifierCV': RidgeClassifierCV(),
        'Perceptron': Perceptron(max_iter=50,penalty='l1'),
        'PassiveAggressiveClassifier': PassiveAggressiveClassifier(),
        'KNeighborsClassifier': KNeighborsClassifier(n_neighbors=50),
        'RandomForestClassifier': RandomForestClassifier(n_estimators=1000),
        'LinearSVC': LinearSVC(dual=False,penalty='l1',tol=1e-3),
        'SGDClassifier': SGDClassifier(alpha=.0001,penalty='l1'),
        'SGDClassifier_elasticnet':SGDClassifier(alpha=.0001,penalty="elasticnet"),
        'NearestCentroid': NearestCentroid(),
        'MultinomialNB': MultinomialNB(alpha=.01),
        'BernoulliNB': BernoulliNB(alpha=.01),
        'ComplementNB': ComplementNB(alpha=.1),
        'SVC':SVC(),
        'LogisticRegression': LogisticRegression(solver='lbfgs',max_iter=5000,penalty='l2'),
        'LogisticRegressionCV' : LogisticRegressionCV(max_iter=5000,n_jobs=-1)
    }

    vectorizers = {
        'hashing': HashingVectorizer(tokenizer=dummy,preprocessor=dummy),
        'count':CountVectorizer(tokenizer=dummy,preprocessor=dummy,max_df=0.5,ngram_range=(1,2),max_features=1000),
        #'glove':GloveTokenize()
    }

    stemmers = {
        'porter' : StemTokenizer(),
        'snowball' : SnowballTokenizer(),
        'lemma' :LemmaTokenizer(),
        # interchangable
        "No Stemmer": dummy,
        None : dummy
    }
    transformers = {
        'tfidf' : TfidfTransformer(use_idf=True,sublinear_tf=True),
        'minmax' : MinMaxScaler(),
        'normal' : Normalizer(norm='l1'),
        'robust' : RobustScaler(),
        'max' : MaxAbsScaler(),
        None : 'passthrough',
        'passthrough' : 'passthrough'
    }

class ExtendedPipeline(Pipeline):


    def __init__(self,
                 classifier : str,
                 vectorizer : str,
                 transformer : bool = None,
                 stemmer : str = None,
                 apply_stemming = True,
                 memory=None,
                 verbose=False):

        if isinstance(stemmer, str):
            self.stemmer = PipelineComponents.stemmers[stemmer]
        else:
            self.stemmer = stemmer
        if isinstance(transformer,str):

            self.transformer = PipelineComponents.transformers[transformer]
        else:
            self.transformer = transformer
        if isinstance(vectorizer,str):
            self.vectorizer = PipelineComponents.vectorizers[vectorizer]
        else:
            self.vectorizer = vectorizer

        stemmer = str(stemmer)
        vectorizer = str(vectorizer)
        transformer = str(transformer)

        if stemmer == None:
            stemmer = "No Stemmer"
            # for cases where text is preprocessed but a stemmer should still be included in the object for later use
            self.apply_stemming = False
        else:
            self.apply_stemming = apply_stemming

        if transformer == None:
            transformer = "No Transformer"

        if isinstance(classifier,str):
            self.classifier = PipelineComponents.models[classifier]
            if transformer != 'No Transformer':
                self.name = (classifier,"_".join([stemmer,vectorizer,transformer]))
                steps = [(vectorizer,self.vectorizer),
                         (transformer,self.transformer),
                         (classifier,self.classifier)]
            else:
                self.name = (classifier,"_".join([stemmer, vectorizer]))
                steps = [(vectorizer,self.vectorizer),
                         (classifier,self.classifier)]

        else:
            self.classifier = classifier
            name = str(classifier)
            clf = name.split('(')[0]
            if transformer:
                self.name = (clf,"_".join([stemmer,vectorizer,transformer]))
                steps = [(vectorizer,self.vectorizer),
                         (transformer,self.transformer),
                         (clf,self.classifier)]
            else:
                self.name = (clf,"_".join([stemmer, vectorizer]))
                steps = [(vectorizer,self.vectorizer),
                         (clf,self.classifier)]

        super().__init__(steps=steps,memory=memory,verbose=verbose)

    def _stem(self,X):
        if self.stemmer:
            if self.apply_stemming:
                Y = []
                for i, text in enumerate(X):
                    Y.append(self.stemmer(text))
                X = Y
        return X

    def decision_function(self, X : Iterable[Any]):
        X = self._stem(X)
        return super().decision_function(X)

    def fit(self,X : Iterable[Any],y=Iterable[Any],**fit_params):
        X = self._stem(X)
        return  super().fit(X,y=y,**fit_params)

    def fit_predict(self, X : Iterable[Any], y : Iterable[Any]=None, **fit_params):
        X = self._stem(X)
        return super().fit_predict(X,y=y,**fit_params)

    def fit_transform(self, X : Iterable[Any], y : Iterable[Any]=None, **fit_params):
        X = self._stem(X)
        return super().fit_transform(X,y=y,**fit_params)

    def transform(self,X):
        X = self._stem(X)
        return super().transform(X)
    def predict(self, X :Iterable[Any], **predict_params):
        X = self._stem(X)
        return super().predict(X,**predict_params)

    def predict_proba(self, X : Iterable[Any]):
        X = self._stem(X)
        return super().predict_proba(X)

    def predict_log_proba(self, X : Iterable[Any]):
        X = self._stem(X)
        return super().predict_log_proba(X)

    def score(self, X : Iterable[Any], y : Iterable[Any]=None, sample_weight=None):
        X = self._stem(X)
        return super().score(X,y,sample_weight)

    def score_samples(self, X : Iterable[Any]):
        X = self._stem(X)
        return super().score_samples(X)

    def save_model(self,fp : Iterable[str] = ('Models')):
        dump(self, os.path.join(os.getcwd(),*fp,f'{self.name}'))