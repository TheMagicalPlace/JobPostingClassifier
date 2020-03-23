"""Adapted from https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py"""


from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.utils.extmath import density
import numpy as np

import pandas as pd
from sklearn.model_selection import GridSearchCV,ParameterGrid,StratifiedKFold
from time import time
from matplotlib import pyplot as plt
import json
from _collections import defaultdict
from  sklearn_extensions.extended_pipeline import *
import warnings
from warnings import simplefilter
import parfit.parfit as pf
from sklearn.metrics import roc_auc_score


def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

class BenchmarkSuite():

    def __init__(self,search_term,X_train,X_test,y_train,y_test,stemmer,vectorizer='count',transform=False):
        """setting up initial data , incl. stemmer,vectorizer, transformer to be benchmarked"""
        self.X_train, self.X_test, self.y_train, self.y_test = X_train,X_test,y_train,y_test
        try:
            with open(os.path.join(os.getcwd(),search_term,'Models','model_stats.json'),'r') as models:
                self.models = json.loads(models.read())
        except FileNotFoundError:
            self.models = defaultdict(list)
        self.stemmer = stemmer
        self.vectorizer = vectorizer
        self.transform = transform
        self.search_term = search_term

    def benchmark_silent(self,clf,feature_names=None,target_names=None,live=False):
        """Benchmarks  without outputting detailed results to console

        Only reports when a model with a higher accuracy is found, reporting model name and accuracy score."""


        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        pred = clf.predict(X_test)
        test_time = time() - t0
        score = metrics.accuracy_score(y_test, pred)
        name = clf.name[0]

        # checking if current iteration is better than current best
        try:
            score_stats = f'Model : {name} | Score : {self.models[name][0]}'
        except IndexError:
            self.models[name] = [score,clf.name[1]]
            dump(clf,os.path.join(os.getcwd(),self.search_term,'Models','model_files',f'{"_".join([clf.name[1],name])}'))
        else:

            if score > self.models[name][0]:
                clf = self.hyperparameter_tuning(name)
                pred = clf.predict(X_test)
                tscore = metrics.accuracy_score(y_test, pred)
                print(f'Original Score : {score}\nTuned Score : {tscore}')
                if score < self.models[name][0]:
                    clf_descr = str(clf).split('(')[0]
                    return clf_descr, score, train_time, test_time
                else:
                    self.models[name] = [score, clf.name[1]]
                    print(score_stats)
                    dump(clf,os.path.join(os.getcwd(),self.search_term,'Models','model_files',f'{"_".join([clf.name[1],name])}'))
        finally:
            clf_descr = str(clf).split('(')[0]
            return clf_descr, score, train_time, test_time

    def benchmark(self,clf,feature_names=None,target_names=None,live=False):
        """Benchmarks and outputs detailed results to console

        Only reports when a model with a higher accuracy is found, returns accuracy, f1 score, model parameters
        and confusion matrix."""
        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        pred = clf.predict(X_test)

        test_time = time() - t0
        score = metrics.accuracy_score(y_test, pred)
        name = clf.name[0]

        try:
            proba = clf.predict_proba(X_test)
            name = clf.name[0]
            #print(name,self.models[name][0])
        except AttributeError:
            pass
        # checking if current iteration is better than current best
        try:
            score_stats = f'Model : {name} | Score : {self.models[name][0]}'
        except IndexError:
            self.models[name] = [score,clf.name[1]]
            dump(clf,os.path.join(os.getcwd(),self.search_term,'Models','model_files',f'{"_".join([clf.name[1],name])}'))

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

        else:
            if score > self.models[name][0]:

                print(clf.name)
                self.models[name] = [score,clf.name[1]]
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



        finally:
            clf_descr = str(clf).split('(')[0]
            return clf_descr, score, train_time, test_time

    def show_results(self,plot=True,silent=False):
        """Runs the data through a preselected series of models and returns results for each"""

        models_to_run  = {model:PipelineComponents.models[model] for model in ['LinearSVC','LogisticRegressionCV','LogisticRegression','Perceptron','RidgeClassifier','SGDClassifier']}
        benchmark = self.benchmark
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
        with open(os.path.join(os.getcwd(),self.search_term,'Models','model_stats.json'),'w') as models:
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

    def hyperparameter_tuning(self,model : str):

        print(f'Tuning {model}')
        t0 = time()
        model = PipelineComponents.models[model]
        pipe = ExtendedPipeline(model,self.vectorizer,transformer=self.transform,stemmer=self.stemmer,apply_stemming=False)
        params = ModelTuningParams.models[pipe.name[0]]
        params_formatted = defaultdict(list)
        name = pipe.name[0]
        for k,v in params.items():
            key_formattted = "__".join([name,k])
            params_formatted[key_formattted] = v
        pgrid = ParameterGrid(params_formatted)

        tuned_pipe = SupressedGSCV(estimator = ExtendedPipeline(model,
                                                               self.vectorizer,
                                                               transformer=self.transform,
                                                               stemmer=self.stemmer,
                                                               apply_stemming=False),
                                  param_grid=params_formatted,
                                  n_jobs=-1,
                                  verbose=0)
        tpipe = tuned_pipe.fit(self.X_train,self.y_train)
        print(tpipe.best_score_)
        print(tpipe.best_params_)
        print(f'Time Elapsed : {time()-t0}')
        return tpipe.best_estimator_
def comparison_decorator(func):
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

class SupressedGSCV(GridSearchCV):
    warnings.filterwarnings("ignore")

    def fit(self, X, y=None, groups=None, **fit_params):
        return super().fit(X,y,groups,**fit_params)