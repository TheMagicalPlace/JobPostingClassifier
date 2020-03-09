from sklearn.pipeline import Pipeline
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC,SVC
from sklearn.preprocessing import MinMaxScaler,MaxAbsScaler,Normalizer,RobustScaler
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier,LogisticRegression,LogisticRegressionCV
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer,CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn_extensions.NLTKUtils import  *
from typing import List,Any,Iterable
from joblib import dump
import os

from numpy import product

def _():
    duals = [True, False]
    penaltys = ['l1', 'l2']
    losses = ['hinge', 'squared_hinge']
    all_params = list(product(duals, penaltys, losses))
    return all_params
def dummy(doc):
    return doc

class ModelTuningParams:
    models= {
        'Perceptron': {
            'penalty': ['l2' ,'l1','elastinet'],
            'max_iter' : [100,1000,5000],
            'tol' : [1e-2,1e-3,1e-4,1e-5],
            'shuffle' : True,
            'eta0' : [0,0.1,1,10],
            'n_jobs' : -1,
            'n_iter' : [10,100,500],
            'early_stopping' : [False,True]
        },
        'RidgeClassifier': {
            'alpha' : [0.1,1,10,100,1000],
            'fit_intercept' : [True,False],
            'max_iter': [-1],#[100, 1000, 5000],
            'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'solver' : ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag'],
        },
        'PassiveAggressiveClassifier':{
            'C': [0.1, 1, 10, 100, 1000],
            'max_iter':[-1],# [100, 1000, 5000],
            'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'early_stopping': [False, True],
            'fit_intercept' : [False,True],
            'loss' : ['hinge','square_hinge'],
            'n_jobs' : [-1],
            'shuffle' : [True]
        },
        'KNeighborsClassifier' : {
            'n_neighbors' : [5,25,50,100],
            'algorithm' : ['auto','ball_tree','kd_tree'],
            'leaf_size' : [10,30,80,125,200],
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
            'max_features' : ['auto','log2',10,100,500,None],
            'max_leaf_nodes' : [10,50,100,None],
            'n_jobs' : [-1]
        },



        'LinearSVC': [{
            'penalty' : ['l1','l2'],
            'loss' : ['hinge','squared_hinge'],
            'C': [0.1, 1, 10, 100, 1000],
            'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'fit_intercept': [False, True],
            'max_iter': [-1],# [100, 1000, 2500],
            'dual' : [True,False]}],
        'SVC' : {
            'C': [0.1, 1, 10, 100, 1000],
            'kernel' : ['rbf','poly','sigmoid'],
            'gamma' : ['scale','auto',0.1,1,10,100],
            'coef0' : [0,0.1,1,10],
            'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'max_iter': [-1], #[100, 1000, 5000,-1],


        },
        'SGDClassifier' : {
            #'alpha': [0.0001,0.001,0.1, 1, 10, 100, 1000],
            'penalty': ['l1', 'l2',"elasticnet"],
            'loss': ['hinge', 'squared_hinge','modified_huber','log','perceptron'],
            #'l1_ratio' : [0.05,0.15,0.3,0.5],
            'fit_intercept': [False, True],
            'max_iter': [100, 1000, 2500],
            #'tol': [1e-2, 1e-3, 1e-4, 1e-5],
            'shuffle' : [True],
            'epsilon' : [0.1,0.5,1,10,100],
            'learning_rate' : ['constant','optimal','invscaling','adaptive'],
            'eta0': [0.01,0.1, 1, 10],
            'early_stopping': [True],
            'power_t' : [0.5]
        },
        'MultinomialNB' : {
            'alpha' : [0.1,1,10,100,1000],
            'fit_prior' : [True,False]
        },
        'BernoulliNB': {
            'alpha': [0.1, 1, 10, 100, 1000],
            'fit_prior': [True, False]
        },
        'ComplimentNB': {
            'alpha': [0.1, 1, 10, 100, 1000],
            'fit_prior': [True, False],
            'norm' : [True,False]
        }
    }



class PipelineComponents:
    models = {
        'RidgeClassifier': RidgeClassifier(tol=1e-2, solver="sag"),
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
        'LogisticRegression': LogisticRegression(solver='liblinear',max_iter=1000,penalty='l1'),
        'LogisticRegressionCV' : LogisticRegressionCV(penalty='l1',solver='liblinear',max_iter=1000,n_jobs=-1)
    }

    vectorizers = {
        'hashing': HashingVectorizer(tokenizer=dummy,preprocessor=dummy),
        'count':CountVectorizer(tokenizer=dummy,preprocessor=dummy,max_df=0.5,ngram_range=(1,2),max_features=10000),
        'glove':GloveTokenize()
    }

    stemmers = {
        'porter' : StemTokenizer(),
        'snowball' : SnowballTokenizer(),
        'lemma' :LemmaTokenizer(),
        None : dummy

    }
    transformers = {
        'tfidf' : TfidfTransformer(use_idf=True,sublinear_tf=True),
        'minmax' : MinMaxScaler(),
        'normal' : Normalizer(norm='l1'),
        'robust' : RobustScaler()
    }

class ExtendedPipeline(Pipeline):


    def __init__(self,
                 classifier : str,
                 vectorizer : str,
                 transformer : bool = False,
                 stemmer : str = None,
                 apply_stemming = True,
                 memory=None,
                 verbose=False):

        if stemmer == None:
            self.stemmer = 'No Stemmer'
            stemmer = 'No Stemmer'
            self.apply_stemming = False
        else:

            # can either use a predefined stemmer or a custom one

            if isinstance(stemmer, str):
                self.stemmer = PipelineComponents.stemmers[stemmer]
            else:
                self.stemmer = stemmer
            stemmer = str(stemmer)

            # for cases where text is preprocessed but a stemmer should still be included in the object for later use
            self.apply_stemming = apply_stemming


        if isinstance(vectorizer,str):
            if vectorizer.lower() == 'glove':
                self.apply_stemming = False
                transformer = False
                self.vectorizer = GloveTokenize()

            else:
                self.vectorizer = PipelineComponents.vectorizers[vectorizer]
            vectorizer = str(vectorizer)

        else:
            self.vectorizer = vectorizer
            vectorizer = str(vectorizer)


        if isinstance(classifier,str):
            self.classifier = PipelineComponents.models[classifier]
            if transformer:
                transform = PipelineComponents.transformers[transformer]
                self.name = (classifier,"_".join([stemmer,vectorizer,transformer]))
                steps = [(vectorizer,self.vectorizer),
                         (transformer,transform),
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
                         (transformer,TfidfTransformer()),
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