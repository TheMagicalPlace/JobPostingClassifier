"""Adapted from https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py"""


from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.utils.extmath import density
import numpy as np
import sqlite3
import pandas as pd
from sklearn.model_selection import GridSearchCV, ParameterGrid, StratifiedKFold, train_test_split
from time import time
from matplotlib import pyplot as plt
import json
from _collections import defaultdict
from  sklearn_extensions.extended_pipeline import *
import warnings
from warnings import simplefilter
import parfit.parfit as pf
from sklearn.metrics import roc_auc_score
import tqdm
from itertools import product


def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

class BenchmarkSuite():

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


    def get_best_model_configs(self):
        active_models = ['LinearSVC',
                          'LogisticRegressionCV',
                          'LogisticRegression',
                          'Perceptron',
                          'RidgeClassifierCV',
                          'SGDClassifier']
        self.best_models = {}
        with self.database:
            cur = self.database.cursor()
            for model in active_models:
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
        train,test = train_test_split(self.dataset,test_size=0.3,stratify = self.dataset.label,shuffle=True)
        self.y_train,self.y_test = train.label.values,test.label.values
        self.X_train,self.X_test = train.description.values,test.description.values

    def training_controller(self, silent=True, plot=False):
        """Runs the data through a preselected series of models and returns results for each"""
        no_labels = len(self.dataset['label'].unique())
        active_models = ['LinearSVC',
                          'LogisticRegressionCV',
                          'LogisticRegression',
                          'Perceptron',
                          'RidgeClassifierCV',
                          'SGDClassifier']
        models_to_run = {model: ExtendedPipeline(model,self.vectorizer,self.transform,self.stemmer,apply_stemming=False)
                         for model in active_models}
        with self.database:
            cur = self.database.cursor()
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

        for _ in tqdm.tqdm(range(self.iterations)):
            self.shuffle_dataset()
            for name,model in models_to_run.items():
                res = self.train_models(model, silent=silent)
                scre = res[2]
                if plot and scre > results[name]['score']:
                    results[name] = res

        for model in active_models:
            uid = self.uid_base + '_' + model
            with self.database:
                cur = self.database.cursor()
                cur.execute("UPDATE model_performance_results SET accuracy = ?,f1_score = ? WHERE unique_id = ?",
                            (self.best_score_ledger[model][0],self.best_score_ledger[model][1],uid))

        if plot==True:

            scores = []
            times = []
            for model_name, best_stats in results.items():
                _, score, training_time, test_time = best_stats
                scores.append(score)
                times.append(np.array(training_time) / np.max(training_time)
                             + np.array(test_time) / np.max(test_time))
            indices = np.arange(len(active_models))

            plt.figure(figsize=(12, 8))
            plt.title("Score")
            plt.barh(indices, scores, .2, label="score", color='navy')
            plt.barh(indices + .3, times, .2, label="run time", color='darkorange')
            plt.yticks(())
            plt.legend(loc='best')
            plt.subplots_adjust(left=.25)
            plt.subplots_adjust(top=.95)
            plt.subplots_adjust(bottom=.05)

            for i, c in zip(indices, active_models):
                plt.text(-.3, i, c)

            plt.show()

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

            clf_descr = str(clf).split('(')[0]
        return clf_descr, accuracy, train_time, test_time

    def show_results(self,plot=True,silent=False):
        """Runs the data through a preselected series of models and returns results for each"""

        models_to_run  = {model:PipelineComponents.models[model] for model in
                          ['LinearSVC',
                           'LogisticRegressionCV','LogisticRegression','Perceptron','RidgeClassifier','SGDClassifier']}
        benchmark = self.train_models
        b_silent = self.benchmark_silent
        results = []
        for nam , clf in models_to_run.items():
            try:
                if silent:
                    pipe = ExtendedPipeline(clf,self.vectorizer,transformer=self.transform,stemmer=self.stemmer,apply_stemming=False)
                    results.append(b_silent(pipe))
                else:
                    pipe = ExtendedPipeline(clf, self.vectorizer, transformer=self.transform, stemmer=self.stemmer,apply_stemming=False)
                    results.append(benchmark(pipe))
            except ValueError as e:
                print(e)
                print('failed')


        indices = np.arange(len(results))

        results = [[x[i] for x in results] for i in range(4)]

        clf_names, score, training_time, test_time = results
        training_time = np.array(training_time) / np.max(training_time)
        test_time = np.array(test_time) / np.max(test_time)

        # saving run results
        with open(os.path.join(os.getcwd(), self.file_term, 'Models', 'model_stats.json'), 'w') as models:
            m = json.dumps(self.models)
            models.write(m)

        # plots run statistics for each model if true, not recommended to be run in combination with iterative benching
        if plot==True:
            plt.figure(figsize=(12, 8))
            plt.title("Score")
            plt.barh(indices, score, .2, label="score", color='navy')
            plt.barh(indices + .3, training_time, .2, label="training time",
                     color='c')
            plt.barh(indices + .6, test_time, .2, label="test time", color='darkorange')
            plt.yticks(())
            plt.legend(loc='best')
            plt.subplots_adjust(left=.25)
            plt.subplots_adjust(top=.95)
            plt.subplots_adjust(bottom=.05)

            for i, c in zip(indices, clf_names):
                plt.text(-.3, i, c)

            plt.show()

    def hyperparameter_tuning(self,model : str,clf=None):
        if model in ['LogisticRegressionCV','RidgeClassifierCV']:
            return clf,0
        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        print(f'Tuning {model}')
        t0 = time()
        name = model
        params = ModelTuningParams.models[name]

        parameters = defaultdict(list)
        for k,v in params.items():
            key_formattted = "__".join([name,k])
            parameters[key_formattted] = v

        base = ExtendedPipeline(model,self.vectorizer,transformer=self.transform,stemmer=self.stemmer,apply_stemming=False)
        base.fit(X_train,y_train)


        tuned_2 = GridSearchCV(estimator=clf,param_grid=parameters,n_jobs=-1,scoring='accuracy')
        tuned_pipe = GridSearchCV(estimator = ExtendedPipeline(model,
                                                               self.vectorizer,
                                                               transformer=self.transform,
                                                               stemmer=self.stemmer,
                                                               apply_stemming=False),
                                  param_grid=parameters,
                                  n_jobs=-1,
                                  verbose=0,
                                   scoring='accuracy')
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

        if ree > re2 and ree > re:
            return base,ree
        elif re > re2:
            return tuned_pipe.best_estimator_,re
        else:
            return tuned_2.best_estimator_,re2




def DEPRECIATED_comparison_decorator(func):
    """Decorator function for comparing the results of the current model settings with previous runs and settings"""
    def wrapper(*args):

        old_data = defaultdict(list)
        # getting previous model stats
        runstat = []
        file_term,iterations,_,_,_ = args
        model_history = defaultdict(list)
        try:
            with open(os.path.join(os.getcwd(), file_term,'Models', 'old', f'model_stats_log.json'), 'r') as models:
                model_history.update(json.loads(models.read()))
                for k, v in model_history.items():
                    runstat = [_ for _ in list(zip(*v))[1]]
                    for it in v:
                        old_data[k].append(it[0])
        except FileNotFoundError:
            pass

        # this should be a function that runs a model + config and saves the results to ./*search_term */Models/...
        func(*args)
        try:
            with open(os.path.join(os.getcwd(), file_term,'Models', 'model_stats.json'), 'r') as models:
                last = json.loads(models.read())
                for k, v in last.items():
                    old_data[k].insert(0,v[0])
                runstat.insert(0,last[k][1])
        except FileNotFoundError as e:
            print(e)
            pass

        current_data = {}
        for k in last.keys():
            current_data[k] = old_data[k]

        # resetting live model stats to none
        os.unlink(os.path.join(os.getcwd(), file_term,'Models', 'model_stats.json'))

        clf = [k for k in last.keys()]

        labels = pd.DataFrame(data=runstat,columns=['Specifications'])
        data = pd.DataFrame(current_data)
        data = labels.join(data)

        print(data.to_string())

        # saving combined model stats
        all_keys = list(model_history.keys())+list(last.keys())
        all_keys = set(all_keys)
        try:
            with open(os.path.join(os.getcwd(), file_term,'Models', 'old', f'model_stats_log.json'), 'w') as models:
                for key in all_keys:
                    try:
                        model_history[key].insert(0, last[key])
                    except KeyError:
                        model_history[key].insert(0,[None,None])
                models.write(json.dumps(model_history))

        except FileNotFoundError:
            model_history = defaultdict(list)
            for key in last.keys():
                model_history[key].insert(0, last[key])
            with open(os.path.join(os.getcwd(), file_term,'Models', 'old', f'model_stats_log.json'), 'w') as models:
                models.write(json.dumps(last))
    return wrapper

