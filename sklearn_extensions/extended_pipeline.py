from sklearn.pipeline import Pipeline
from sklearn.linear_model import RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import HashingVectorizer,CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn_extensions.NLTKUtils import  *
from typing import List,Any,Iterable
from joblib import dump
import os


def dummy(doc):
    return doc

class PipelineComponents:
    models = {
        'RidgeClassifier': RidgeClassifier(tol=1e-2, solver="sag"),
        'Perceptron': Perceptron(max_iter=50),
        'PassiveAggressiveClassifier': PassiveAggressiveClassifier(max_iter=50),
        'KNeighborsClassifier': KNeighborsClassifier(n_neighbors=10),
        'RandomForestClassifier': RandomForestClassifier(),
        'LinearSVC': LinearSVC(penalty='l2', dual=False,tol=1e-3),
        'SGDClassifier': SGDClassifier(alpha=.0001, max_iter=50,penalty='l2'),
        'SGDClassifier_elasticnet':SGDClassifier(alpha=.0001, max_iter=50,penalty="elasticnet"),
        'NearestCentroid': NearestCentroid(),
        'MultinomialNB': MultinomialNB(alpha=.01),
        'BernoulliNB': BernoulliNB(alpha=.01),
        'ComplementNB': ComplementNB(alpha=.1)
    }

    vectorizers = {
        'hashing': HashingVectorizer(tokenizer=dummy,preprocessor=dummy),
        'count':CountVectorizer(tokenizer=dummy,preprocessor=dummy),
    }

    stemmers = {
        'porter' : StemTokenizer(),
        'snowball' : SnowballTokenizer(),
        'lemma' :LemmaTokenizer()

    }
    transformers = {
        'tfidf' : TfidfTransformer()
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
        if stemmer is not None:
            # for cases where text is preprocessed but a stemmer should still be included in the object for later use
            self.apply_stemming = apply_stemming

            # can either use a predefined stemmer or a custom one
            if isinstance(stemmer,str):
                self.stemmer = PipelineComponents.stemmers[stemmer]
            else:
                self.stemmer = stemmer
        else:
            self.stemmer = None

        if isinstance(vectorizer,str):
            self.vectorizer = PipelineComponents.vectorizers[vectorizer]
        else:
            self.vectorizer = vectorizer
            vectorizer = str(vectorizer)

        if isinstance(classifier,str):
            self.classifier = PipelineComponents.models[classifier]
            if transformer:
                transform = PipelineComponents.transformers['tfidf']
                self.name = (classifier,"_".join([stemmer,vectorizer,'with_transform']))
                steps = [(vectorizer,self.vectorizer),
                         ('transform',transform),
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
                self.name = (clf,"_".join([stemmer,vectorizer,'with_transform']))
                steps = [(vectorizer,self.vectorizer),
                         ('transform',TfidfTransformer()),
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