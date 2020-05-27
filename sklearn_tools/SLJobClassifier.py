import sqlite3
from abc import ABC, abstractmethod
from itertools import product
import os
import imblearn
import pandas as pd
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QRunnable, QObject
from joblib import load

from sklearn_tools import PipelineComponents
from sklearn_tools import ClassificationTrainingTool


class Error(Exception):
    pass

class ModeMismatch(Error):
    """Exception for invalid method-mode combination in some of the following classes"""
    def __init__(self, method_name, mode, *args):
        self.message = f" ModeMismatchError : Current method '{method_name}' does not support mode '{mode}'"
        super().__init__(self.message)
        # Special attribute you desire with your Error,
        # perhaps the value that caused the error?:
        # allow users initialize misc. arguments as any other builtin Error

class TextClassificationABC(ABC):
    """Abstract base class for text classification oriented scikit-learn models."""

    @abstractmethod
    def __init__(self,file_term : str,
                 database,
                 mode : str = 'train'):
        self.file_term = file_term
        self.database = database
        if mode in ['train','tune']:
            self.dataset = pd.read_sql(f"SELECT label,description from training",self.database)
        elif mode == 'live':
            self.dataset = pd.read_sql(f"SELECT unsorted.unique_id,unsorted.description,unsorted.job_title,metadata.location "
                                       f"FROM unsorted "
                                       f"INNER JOIN metadata ON unsorted.unique_id = metadata.unique_id",self.database)
            self.dataset.insert(0,'label',0)

    @abstractmethod
    def _text_preprocessing(self):
        pass

    @abstractmethod
    def classify_results(self,*args,**kwargs):
        pass

class ClassificationHandler(TextClassificationABC):
    """ Handler class for the classification job descriptions.

    One important thing to note is that training a configuration and them using the results to predict unlabeled
    data is not supported. Specifically the 'table' parameter decides """


    job_label_associations = {'Good Jobs':'Good', 'Bad Jobs':'Bad', 'Neutral Jobs':'Bad', 'Ideal Jobs':'Good'}

    def __init__(self, file_term : str,
                 database,
                 mode,
                 no_labels : int,
                 stemmer : str = None,
                 vectorizer : str ='count',
                 transform : str =None,
                  ):
        super().__init__(file_term=file_term,database=database,mode=mode)
        self.catagories = no_labels
        # setting up number of catagories used in classification
        if no_labels == 2:
            self.job_label_associations = {'Good Jobs':'Good',
                                           'Bad Jobs':'Bad',
                                           'Neutral Jobs':'Bad',
                                           'Ideal Jobs':'Good'}
        elif no_labels == 3:
            self.job_label_associations = {'Good Jobs': 'Good',
                                           'Bad Jobs': 'Bad',
                                           'Neutral Jobs': 'Neutral',
                                           'Ideal Jobs': 'Good'}
        else:
            self.job_label_associations = ClassificationHandler.job_label_associations

        self.stemmer = stemmer
        self.vectorizer = vectorizer
        self.transform = transform


        # live sorting uses pickled models , so no customization of text processing is allowed
        if mode in ['train','tune']:
            self.mode = mode
            self.dataset = self.dataset[self.dataset.label.isin([_ for _ in self.job_label_associations.keys()])]
            self._text_preprocessing()
        elif mode == 'live':
            self.mode = mode

    def classify_results(self,model):
        """ Sorts job descriptions generated during actual use of the program"""

        model.apply_stemming = True if model.stemmer != "No Stemmer" else False

        with self.database:
            cur = self.database.cursor()
            for i,data in self.dataset.iterrows():
                live_text = data.location+'\n'+data.description
                label = model.predict([live_text])[0]+" Jobs"
                cur.execute("INSERT INTO results VALUES (?,?,?,?)",(data.unique_id,
                                                                    label,
                                                                    data.job_title,
                                                                    data.description))
                cur.execute("DELETE FROM unsorted WHERE unique_id = ?",(data.unique_id,))


    def _text_preprocessing(self):
        '''Processes the text files to remove punctuation, noise (i.e url's), and case from the text
         and assignes the result to a pandas dataframe containing the label and content'''

        stemmer = PipelineComponents.stemmers[self.stemmer]
        job_cat_data = {}

        paths = {}
        over = imblearn.over_sampling.RandomOverSampler()
        valid_labels = set([_ for _ in self.job_label_associations.keys()])
        for iter,row in self.dataset.iterrows():
            if self.dataset['label'][iter] not in valid_labels:
                self.dataset.drop(iter)
            self.dataset['label'][iter] = self.job_label_associations[row[0]]
            self.dataset['description'][iter] = stemmer(row[1])




class ClassificationInterface():
    """Middleman class for interfacing between external callers (i.e. UI's) and the classification handler classes"""
    def __init__(self,file_term,iterations,mode='train',no_labels=2,tuning_frequency = 'minimal'):
        self.no_labels = no_labels
        self.mode = mode
        self.file_term = file_term
        self.iterations = iterations
        self.database = sqlite3.connect(os.path.join(os.getcwd(),file_term,f'{file_term}.db'))
        self.tuning_frequency = tuning_frequency


    def qt_progress_signal_manager(self,vectorizer,transformer,stemmer,round,total_rounds):
       """ Dummy method to be overwritten by QT (or other threading interface) enabled child classes"""
       pass

    def train_models(self,silent=True,plot=False,*exclude):
        """Runs the training process based on inputs"""
        if self.mode != 'train':
            raise ModeMismatch(ClassificationInterface.train_models.__name__,self.mode)
        count = 0
        combos = list(product(['count'],[None,'normal','max','tfidf'],['porter','snowball','lemma',None]))

        # this is largely based on what I found to provide the best results, and will
        # likely be changed to be dynamic in a future release
        for vectorizer in ['count']:
            for transformer in [None,'normal','max','tfidf']:
                for stemmer in ['porter','snowball','lemma',None]:
                    if vectorizer in exclude or stemmer in exclude or transformer in exclude:
                        continue
                    else:
                        search = ClassificationHandler(self.file_term,
                                                       self.database,
                                                       mode='train',
                                                       no_labels=self.no_labels,
                                                       vectorizer=vectorizer,
                                                       stemmer=stemmer,
                                                       transform=transformer)
                        bench = ClassificationTrainingTool(self.file_term, search, self.iterations)
                        bench.training_controller(silent=silent, plot=plot)
                        count+=1
                        self.qt_progress_signal_manager(vectorizer,transformer,stemmer,round=count,total_rounds=combos.__len__())
        else:
            if self.tuning_frequency == 'minimal':
                self.mode = 'tune'
                self.tune_models()

    def classify_live_jobs(self):
        """ Classifies jobs using the best model for the current file using the
        corresponding method in the ClassificationHandler."""

        if self.mode != 'live':
            raise ModeMismatch(ClassificationInterface.classify_live_jobs.__name__,self.mode)
        with self.database:
            cur = self.database.cursor()
            model = cur.execute("""SELECT MAX(accuracy),unique_id from model_performance_results 
                            WHERE classification_labels = ?""",(self.no_labels,)).fetchone()
            model_id = list(model)[1]

        model = load(os.path.join(os.getcwd(),self.file_term,'models',model_id))
        #print(os.path.join(os.getcwd(),self.file_term,'models',model_id))
        #with open(os.path.join(os.getcwd(),self.file_term,'models',model_id), 'rb') as pickle_file:
        #    model = load(pickle_file)


        clfh = ClassificationHandler(self.file_term,self.database,self.mode,self.no_labels)
        clfh.classify_results(model)

    def tune_models(self):
        """Tunes the best models using a cross-validation approach provided by the ClassificationTrainingTool class"""
        if self.mode != 'tune':
            raise ModeMismatch(ClassificationInterface.tune_models.__name__,self.mode)
        with self.database:
            cur = self.database.cursor()
            for model in cur.execute("""SELECT MAX(accuracy),model,unique_id,stemmer from model_performance_results
                            WHERE classification_labels = ? GROUP BY model""",(self.no_labels,)):
                    score_to_beat,name,unique_id,stemmer = model

                    model = load(os.path.join(os.getcwd(),self.file_term,'models',unique_id))
                    clf_handler = ClassificationHandler(self.file_term,self.database,no_labels=self.no_labels,
                                                        stemmer=stemmer,mode=self.mode)
                    bench = ClassificationTrainingTool(self.file_term, clf_handler, 1)
                    clf,score = bench.hyperparameter_tuning(name,model)
                    if score >score_to_beat:
                        cur.execute("""UPDATE model_performance_results SET accuracy = ? WHERE unique_id = ?""",(score,unique_id))

class QWorkerCompatibleClassificationInterface(ClassificationInterface,QRunnable):
    """Qt Threading enabled version of the Classification Interface. """
    class Signals(QObject):
        progress = pyqtSignal(int)
        params = pyqtSignal(tuple)
        finished = pyqtSignal()

    def __init__(self,file_term,iterations,mode='train',no_labels=2,tuning_frequency = 'minimal'):
        QRunnable.__init__(self)
        super().__init__(file_term,iterations,mode=mode,no_labels=no_labels,tuning_frequency =tuning_frequency)
        self.signals = QWorkerCompatibleClassificationInterface.Signals()

    @pyqtSlot()
    def train_models(self,silent=False,plot=False,*exclude):
        super().train_models(silent,plot,exclude)

    @pyqtSlot()
    def run(self):
        """QtRunnable compliant training handler. Runs desired process based on the 'mode' flag and the
        given file term."""
        self.database = sqlite3.connect(os.path.join(os.getcwd(), self.file_term, f'{self.file_term}.db'))
        if self.mode =='train':
            self.train_models()
        elif self.mode == 'tune':
            self.tune_models()
        elif self.mode == 'live':
            self.classify_live_jobs()
        self.signals.finished.emit()

    @pyqtSlot()
    def qt_progress_signal_manager(self, vectorizer, transformer, stemmer, round, total_rounds):
        """ Sends training status back to the GUI"""
        self.signals.progress.emit(int(100*round/total_rounds))
        self.signals.params.emit((stemmer,vectorizer,transformer))
        pass

if __name__ == '__main__':
    p = list(product(['count'], [None, 'normal', 'max', 'tfidf'], ['porter', 'snowball', 'lemma', None]))
    #clf = ClassificationInterface('Chemical Engineer',10,mode='tune')
    #clf.tune_models()
    e = QWorkerCompatibleClassificationInterface('../Chemical Engineer', 100)
    print(QWorkerCompatibleClassificationInterface.__mro__,QWorkerCompatibleClassificationInterface.__dict__)
    print('s')











