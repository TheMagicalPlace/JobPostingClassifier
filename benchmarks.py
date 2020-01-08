"""Taken from https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py"""


from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
import numpy as np
from time import time
from matplotlib import pyplot as plt
def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."
class BenchmarkSuite():

    def __init__(self,X_train,X_test,y_train,y_test):
        self.X_train, self.X_test, self.y_train, self.y_test = X_train,X_test,y_train,y_test

    def benchmark(self,clf,feature_names=None,target_names=None):
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
        return clf_descr, score, train_time, test_time

    def show_results(self,plot=True):
        benchmark = self.benchmark
        results = []
        for clf, name in (
                (RidgeClassifier(tol=1e-2, solver="sag"), "Ridge Classifier"),
                (Perceptron(max_iter=50), "Perceptron"),
                (PassiveAggressiveClassifier(max_iter=50),
                 "Passive-Aggressive"),
                (KNeighborsClassifier(n_neighbors=10), "kNN"),
                (RandomForestClassifier(), "Random forest")):
            print('=' * 80)
            print(name)
            results.append(benchmark(clf))

        for penalty in ["l2", "l1"]:
            print('=' * 80)
            print("%s penalty" % penalty.upper())
            # Train Liblinear model
            results.append(benchmark(LinearSVC(penalty=penalty, dual=False,
                                               tol=1e-3)))

            # Train SGD model
            results.append(benchmark(SGDClassifier(alpha=.0001, max_iter=50,
                                                   penalty=penalty)))

        # Train SGD with Elastic Net penalty
        print('=' * 80)
        print("Elastic-Net penalty")
        results.append(benchmark(SGDClassifier(alpha=.0001, max_iter=50,
                                               penalty="elasticnet")))

        # Train NearestCentroid without threshold
        print('=' * 80)
        print("NearestCentroid (aka Rocchio classifier)")
        results.append(benchmark(NearestCentroid()))

        # Train sparse Naive Bayes classifiers
        print('=' * 80)
        print("Naive Bayes")
        results.append(benchmark(MultinomialNB(alpha=.01)))
        results.append(benchmark(BernoulliNB(alpha=.01)))
        results.append(benchmark(ComplementNB(alpha=.1)))

        print('=' * 80)
        print("LinearSVC with L1-based feature selection")
        # The smaller C, the stronger the regularization.
        # The more regularization, the more sparsity.
        results.append(benchmark(Pipeline([
          ('feature_selection', SelectFromModel(LinearSVC(penalty="l1", dual=False,
                                                          tol=1e-3))),
          ('classification', LinearSVC(penalty="l2"))])))

        indices = np.arange(len(results))

        results = [[x[i] for x in results] for i in range(4)]

        clf_names, score, training_time, test_time = results
        training_time = np.array(training_time) / np.max(training_time)
        test_time = np.array(test_time) / np.max(test_time)
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
