"""Taken from https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py"""


from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.utils.extmath import density
import numpy as np
from time import time
from matplotlib import pyplot as plt
import json
from _collections import defaultdict
from  sklearn_extensions.extended_pipeline import *
import warnings
warnings.filterwarnings("ignore")
def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."
class BenchmarkSuite():

    def __init__(self,X_train,X_test,y_train,y_test):
        self.X_train, self.X_test, self.y_train, self.y_test = X_train,X_test,y_train,y_test
        try:
            with open(os.path.join(os.getcwd(),'Models','model_stats.json'),'r') as models:
                self.models = json.loads(models.read())
        except FileNotFoundError:
            self.models = defaultdict(int)

    def benchmark_silent(self,clf,feature_names=None,target_names=None,live=False):

        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        pred = clf.predict(X_test)
        test_time = time() - t0
        score = metrics.accuracy_score(y_test, pred)
        name = clf.name
        print(f'Score : {score} | Best : {self.models[name]}')
        if score > self.models[name]:
            self.models[name] = score
            print('Valid Candidate Found')
            dump(clf,f'./Models/{name}')
        clf_descr = str(clf).split('(')[0]
        return clf_descr, score, train_time, test_time

    def benchmark(self,clf,feature_names=None,target_names=None,live=False):
        X_train, X_test, y_train, y_test = self.X_train, self.X_test, self.y_train, self.y_test
        print('_' * 80)
        print("Training: ")
        print(clf)
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        print("train time: %0.3fs" % train_time)

        t0 = time()
        pred = clf.predict(X_test)
        test_time = time() - t0
        print("test time:  %0.3fs" % test_time)

        score = metrics.accuracy_score(y_test, pred)
        print("accuracy:   %0.3f" % score)
        name = str(clf)
        name = name.split('(')[0]
        print(f'Score : {score} | Best : {self.models[name]}')
        if score > self.models[name]:
            self.models[name] = score
            print('Valid Candidate Found')
            dump(clf,f'./Models/{name}')

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

        print()
        clf_descr = str(clf).split('(')[0]
        if live:
            return clf
        return clf_descr, score, train_time, test_time

    def show_results(self,plot=True,silent=False):
        models_to_run = \
            [
                RidgeClassifier(tol=1e-2, solver="sag"),
                Perceptron(max_iter=50),
                PassiveAggressiveClassifier(max_iter=50),
                KNeighborsClassifier(n_neighbors=10),
                RandomForestClassifier(),
                LinearSVC(penalty='l1', dual=False,
                          tol=1e-3),
                LinearSVC(penalty='l2', dual=False,
                          tol=1e-3),

                SGDClassifier(alpha=.0001, max_iter=50,
                              penalty='l1'),
                SGDClassifier(alpha=.0001, max_iter=50,
                              penalty='l2'),
                SGDClassifier(alpha=.0001, max_iter=50,
                              penalty="elasticnet"),
                NearestCentroid(),
                MultinomialNB(alpha=.01),
                BernoulliNB(alpha=.01),
                ComplementNB(alpha=.1),
            ]

        benchmark = self.benchmark
        b_silent = self.benchmark_silent
        results = []

        for clf in models_to_run:
            if silent:
                pipe = ExtendedPipeline(clf,'count',transformer=False,stemmer='snowball',apply_stemming=False)
                results.append(b_silent(pipe))
            else:
                pipe = ExtendedPipeline(clf, 'count', transformer=False, stemmer='snowball',apply_stemming=False)
                results.append(benchmark(pipe))



        indices = np.arange(len(results))

        results = [[x[i] for x in results] for i in range(4)]

        clf_names, score, training_time, test_time = results
        training_time = np.array(training_time) / np.max(training_time)
        test_time = np.array(test_time) / np.max(test_time)
        with open(os.path.join(os.getcwd(),'Models','model_stats.json'),'w') as models:
            m = json.dumps(self.models)
            models.write(m)
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
