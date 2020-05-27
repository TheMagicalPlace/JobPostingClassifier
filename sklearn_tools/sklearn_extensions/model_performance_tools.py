"""Adapted from https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py"""


import json
import os
import sqlite3
from _collections import defaultdict
from time import time
from statistics import mean

import numpy as np
import pandas as pd
import tqdm
from joblib import dump

from sklearn import metrics
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.utils.extmath import density

from sklearn_tools import ExtendedPipeline, PipelineComponents, ModelTuningParams


def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

class ClassificationTrainingTool():

    def __init__(self, file_term, classification_handler,iterations,tuning_depth : str = 'minimal'):

        """setting up initial data , incl. stemmer,vectorizer, transformer to be benchmarked

        attributes:
            file_term - the name of the file folder the database and models are located in
            classification_handler - container for keeping track of training data and model configurations
            iterations - number of iterations to run during training for each model
            tuning_complexity (None,'minimal','regular','max') - how often the best found model should be tuned using
            GridSearchCV

        """
        self.tuning_depth = tuning_depth
        self.database = classification_handler.database
        self.dataset = classification_handler.dataset
        self.stemmer = classification_handler.stemmer
        self.vectorizer = classification_handler.vectorizer
        self.transform = classification_handler.transform
        self.iterations = iterations
        self.file_term = file_term
        self.shuffle_dataset()
        self.uid_base = "_".join([str(len(self.dataset['label'].unique())),str(self.stemmer),str(self.transform),str(self.vectorizer)])
        self.best_score_ledger = {}
        self.active_models =['LinearSVC',
                          #'LogisticRegressionCV',
                          'LogisticRegression',
                          'Perceptron',
                          #'RidgeClassifierCV',
                          'SGDClassifier',
                         #'PassiveAggressiveClassifier',
                         'ElasticNetClassifier',
                         'RandomForestClassifier',
                             #'XGBClassifier',
            ]

    def get_best_model_configs(self):
        """Sets the 'to-beat' model score for each classification method, used by the training controller
        to determine when a model is better than the previous best."""
        self.best_models = {}
        with self.database:
            cur = self.database.cursor()
            for model in self.active_models:
                if self.tuning_depth == 'minimal':
                    a = cur.execute("SELECT MAX(accuracy),unique_id from model_performance_results")
                elif self.tuning_depth == 'normal':
                    a = cur.execute("SELECT MAX(accuracy),unique_id from model_performance_results WHERE model = ?",
                                    (model,))
                elif self.tuning_depth == 'maximal':
                    a = cur.execute("SELECT MAX(accuracy),unique_id from model_performance_results WHERE model = ?",
                                    (model,))
                    # TODO not implimented, same as normal
                self.best_models[model] = list(a)[0][0]

    def shuffle_dataset(self):
        """ Splits the presorted job data for model training"""
        # TODO explain approached used for selecting training and test data
        labels = self.dataset.label.unique()
        good_jobs = self.dataset[self.dataset.label == "Good"]
        bad_jobs = self.dataset[self.dataset.label == "Bad"]

        # TODO n>2 probablly won't work the way it's supposed to currently
        if len(labels) == 2:
            # oversample
            resize = max(len(good_jobs.label),len(bad_jobs.label))
            # undersample
            resize =  min(len(good_jobs.label), len(bad_jobs.label))
            good_jobs_re = good_jobs.sample(resize)
            bad_jobs_re = bad_jobs.sample(resize)
            dataset = pd.concat([good_jobs_re, bad_jobs_re])
        elif len(labels) == 3:
            neutral_jobs = self.dataset[self.dataset.label == "Neutral"]
            # oversample
            resize = max(len(good_jobs.label), len(bad_jobs.label),len(neutral_jobs.label))
            # undersample
            resize = min(len(good_jobs.label), len(bad_jobs.label),len(neutral_jobs.label))

            good_jobs_re = good_jobs.sample(resize, replace=True)
            bad_jobs_re = bad_jobs.sample(resize, replace=True)
            neutral_jobs_re = bad_jobs.sample(resize, replace=True)
            dataset = pd.concat([good_jobs_re, bad_jobs_re,neutral_jobs_re])
        elif len(labels) == 4:
            neutral_jobs = self.dataset[self.dataset.label == "Neutral"]
            ideal_jobs = self.dataset[self.dataset.label == "Ideal"]

            # middle of the road approach
            resize = int(mean([len(good_jobs.label), len(bad_jobs.label),len(neutral_jobs.label),len(ideal_jobs.label)]))
            good_jobs_re = good_jobs.sample(resize, replace=True)
            bad_jobs_re = bad_jobs.sample(resize, replace=True)
            neutral_jobs_re = bad_jobs.sample(resize, replace=True)
            ideal_jobs_re = ideal_jobs.sample(resize,replace=True)
            dataset = pd.concat([good_jobs_re, bad_jobs_re,neutral_jobs_re,ideal_jobs_re])

        train,test = train_test_split(dataset,test_size=0.25,stratify = dataset.label,shuffle=True)
        #test = self.dataset[~self.dataset.isin(train)].dropna()
       #test = self.dataset[(~dataset.label.isin(self.dataset.label))&(~dataset.description.isin(self.dataset.description))]
        #0tr_hashes = [hash(tuple(d)) for d in train.description]
        #ytest = [val for iter,val in self.dataset.iterrows() if hash(tuple(val.description)) not in tr_hashes]

        self.y_train,self.y_test = train.label.values,test.label.values
        self.X_train,self.X_test = train.description.values,test.description.values

    def ignore_suboptimal_combinations(self,active_models):
        """Combinations that consistently produce comparatively bad results are ignored."""
        if self.transform =='max':
            not_trained = ['ElasticNetClassifier',
                          'PassiveAggressiveClassifier',
                           'RidgeClassifierCV',]
        elif self.transform =='normal':
            not_trained = ['ElasticNetClassifier',
                          'PassiveAggressiveClassifier',
                           'SDGClassifier',
                           'LinearSVC',
                           'RidgeClassifierCV',
                            'LogisticRegression',]
        elif self.transform == 'tfidf':
            not_trained = ['ElasticNetClassifier',
                          'PassiveAggressiveClassifier',
                           'RidgeClassifierCV',
                            'LogisticRegression',]
        else:
            not_trained = []
        active_models = [model for model in active_models if model not in not_trained]
        return active_models

    def training_controller(self, silent=True, plot=False):
        """Runs the data through a preselected series of models and returns results for each"""
        no_labels = len(self.dataset['label'].unique())
        active_models = self.active_models
        active_models = self.ignore_suboptimal_combinations(active_models)
        models_to_run = {model: ExtendedPipeline(model,self.vectorizer,self.transform,self.stemmer,apply_stemming=False)
                         for model in active_models}
        with self.database:
            cur = self.database.cursor()

            # if there is no data for the current training settings, create an entry in the table
            for model in active_models:
                uid = self.uid_base+'_'+model
                try:
                    cur.execute("INSERT INTO model_performance_results VALUES (?,?,?,?,?,0,0,?)",
                                (uid,self.stemmer,self.vectorizer,self.transform,model,no_labels))
                    self.best_score_ledger[model] = [0, 0]
                except sqlite3.IntegrityError:
                    scores_to_beat = cur.execute("""SELECT f1_score,accuracy from model_performance_results
                                                               WHERE unique_id = ? """,
                                                              (self.uid_base+'_'+model,))
                    self.best_score_ledger[model] = [_ for _ in list(scores_to_beat)[0]]

        self.get_best_model_configs()
        results = defaultdict(dict)

        # run n iterations for each model in this configuration
        for _ in tqdm.tqdm(range(self.iterations)):
            if not silent:
                print(f'\nRound {_}:\nStemmer : {self.stemmer}\nTransformer : {self.transform}\n')
            self.shuffle_dataset()
            for name,model in models_to_run.items():
                res = self.train_models(model, silent=silent)
                scre = res[2]
                if plot and scre > results[name]['score']:
                    results[name] = res

        # updating model performance results table
        for model in active_models:
            uid = self.uid_base + '_' + model
            with self.database:
                cur = self.database.cursor()
                cur.execute("UPDATE model_performance_results SET accuracy = ?,f1_score = ? WHERE unique_id = ?",
                            (self.best_score_ledger[model][0],self.best_score_ledger[model][1],uid))



    def train_models(self, clf, silent, feature_names=None, target_names=None, live=False):
        """Benchmarks and outputs detailed results to console

        Only reports when a model with a higher accuracy is found, returns accuracy, f1 score, model parameters
        and confusion matrix."""
        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        pred = clf.predict(X_test)
        test_time = time() - t0
        accuracy = metrics.accuracy_score(y_test, pred)
        fbeta = metrics.fbeta_score(y_test, pred,1,labels=self.dataset['label'].unique(),average='weighted')
        name = clf.name[0]
        if False:
            score_stats = f'Model : {name} | Score : {accuracy} | F-beta : {fbeta}'
            print(score_stats)

        if self.best_score_ledger[name][0] < accuracy:
            last = self.best_score_ledger[name][0]
            print(name)
            self.best_score_ledger[name] = [accuracy,fbeta]
            score_stats = f'Model : {name} | Score : {accuracy} | F-beta : {fbeta}'
            print(self.stemmer, ' ', self.transform)
            print(score_stats)

            if accuracy > self.best_models[name] and last != 0.0 and self.tuning_depth in ['normal','maximal']:
                new_model,score = self.hyperparameter_tuning(name,clf)
                if score > accuracy:
                    self.best_score_ledger[name][0] = score
                    clf = new_model
            dump(clf, os.path.join(os.getcwd(), self.file_term, 'models', f'{"_".join([self.uid_base, name])}'))



            if not silent:
                if hasattr(clf, 'coef_'):
                    print("dimensionality: %d" % clf.coef_.shape[1])
                    print("density: %f" % density(clf.coef_))

                    if True and feature_names is not None:
                        print("top 10 keywords per class:")
                        for i, label in enumerate(target_names):
                            top10 = np.argsort(clf.coef_[i])[-10:]
                            print(trim("%s: %s" % (label, " ".join(feature_names[top10]))))
                    print()

                if True:
                    print("classification report:")
                    print(metrics.classification_report(y_test, pred,
                                                        target_names=target_names))

                if True:
                    print("confusion matrix:")
                    print(metrics.confusion_matrix(y_test, pred))
        # if no model exists for the current settings, create one by default. Prevents issues if models are deleted.
        elif not os.path.exists(
                os.path.join(os.getcwd(), self.file_term, 'models', f'{"_".join([self.uid_base, name])}')):
            dump(clf, os.path.join(os.getcwd(), self.file_term, 'models', f'{"_".join([self.uid_base, name])}'))
        clf_descr = str(clf).split('(')[0]
        return clf_descr, accuracy, train_time, test_time

    def hyperparameter_tuning(self,model : str,clf=None):
        # NOT INCLUDED IN RELEASE DUE TO ISSUES WITH MULTIPROCESSING
        if True:
            return clf

        """Tuning of parameters to valid models using a cross-validation approach (GridSearchCV)"""
        if model in ['LogisticRegressionCV','RidgeClassifierCV','XGBClassifier','ElasticNetClassifier']:
            return clf,0
        self.shuffle_dataset()
        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        print(f'Tuning {model}')
        t0 = time()
        name = model
        params = ModelTuningParams.models[name]

        parameters = defaultdict(list)
        for k,v in params.items():
            key_formattted = "__".join([name,k])
            parameters[key_formattted] = v

        # baseline model, should be the same as the input model in most cases
        base = ExtendedPipeline(model,self.vectorizer,transformer=self.transform,stemmer=self.stemmer,apply_stemming=False)
        base.fit(X_train,y_train)

        # two tuning approaches
        tuned_2 = GridSearchCV(estimator=clf,param_grid=parameters,n_jobs=-1,scoring='f1')
        tuned_pipe = GridSearchCV(estimator = ExtendedPipeline(model,
                                                               self.vectorizer,
                                                               transformer=self.transform,
                                                               stemmer=self.stemmer,
                                                               apply_stemming=False),
                                  param_grid=parameters,
                                  n_jobs=-1,
                                  verbose=0,
                                   scoring='f1')
        tuned_2.fit(X_train,y_train)
        tuned_pipe.fit(X_train,y_train)
        r = tuned_pipe.predict(X_test)
        r2 = tuned_2.predict(X_test)
        print(f'Time Elapsed : {time()-t0}')
        print(f'unmodified : {metrics.accuracy_score(y_test,base.predict(X_test))} original new : {metrics.accuracy_score(y_test,r)}\n old new : {metrics.accuracy_score(y_test,r2)}')

        ree = metrics.accuracy_score(y_test,base.predict(X_test))
        re = metrics.accuracy_score(y_test,r)
        re2 = metrics.accuracy_score(y_test,r2)
        print(tuned_pipe.best_score_)
        print(tuned_2.best_score_)

        # return best results
        if ree > re2 and ree > re:
            return base,ree
        elif re > re2:
            return tuned_pipe.best_estimator_,re
        else:
            return tuned_2.best_estimator_,re2

