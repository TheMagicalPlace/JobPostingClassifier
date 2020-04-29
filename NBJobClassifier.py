from sklearn.model_selection import train_test_split
from sklearn_extensions.benchmarks import *
from sklearn_extensions.NLTKUtils import *
from sklearn_extensions.featurization import *
from sklearn_extensions.extended_pipeline import PipelineComponents
from joblib import load
import sqlite3
import pandas as pd

class ClassificationHandler:

    job_label_associations = {'Good Jobs':'Good', 'Bad Jobs':'Bad', 'Neutral Jobs':'Neutral', 'Ideal Jobs':'Good'}

    def __init__(self,search_term : str,database,stemmer : str = None,vectorizer='count',transform=False,training=True,):
        self.search_term = search_term
        self.database = database
        self.dataset = pd.read_sql("SELECT label,description from training",self.database)
        print(self.dataset)
        self.stemmer = stemmer


        # live sorting uses pickled models , so no customization of text processing is allowed
        if training:
            self._jobdesc_preprocessing()
            self.vectorizer = vectorizer
            self.transform = transform

    def _jobdesc_preprocessing(self):
        '''Processes the text files to remove punctuation, noise (i.e url's), and case from the text
         and assignes the result to a pandas dataframe containing the label and content'''

        stemmer = PipelineComponents.stemmers[self.stemmer]
        job_cat_data = {}
        paths = {}
        for iter,row in self.dataset.iterrows():
            self.dataset['label'][iter] = self.job_label_associations[row[0]]
            self.dataset['description'][iter] = stemmer(row[1])

    def _split_dataset(self):
        """ Splits the presorted job data for model training"""
        train,test = train_test_split(self.dataset,test_size=0.3,stratify = self.dataset.label,shuffle=True)
        y_train,y_test = train.label.values,test.label.values
        X_train,X_test = train.description.values,test.description.values
        self.X_train,self.X_test = X_train,X_test
        self.y_train,self.y_test = y_train,y_test

    def model_data(self,iterations):
        self._split_dataset()
        bench = BenchmarkSuite(self.search_term,self)
        bench.benchmark_controller(iterations,plot=False)
        return 'None'


    def tune_model(self,model : str):
        self._split_dataset()
        bench = BenchmarkSuite(self.search_term, self.X_train, self.X_test, self.y_train, self.y_test,
                               stemmer=self.stemmer, vectorizer=self.vectorizer, transform=self.transform)
        bench.hyperparameter_tuning(model)
        return 'done'

class ClassificationInterface():

    def __init__(self,file_term,iterations):
        self.file_term = file_term
        self.iterations = iterations
        self.database = sqlite3.connect(os.path.join(os.getcwd(),file_term,f'{file_term}.db'))


    def train_models(self,*exclude):


        def __run_search(file_term,iterations,stemmer,vectorizer,transformer):
            search = ClassificationHandler(self.file_term,
                                           self.database,
                                           vectorizer=vectorizer,
                                           stemmer=stemmer,
                                           transform=transformer)
            bench = BenchmarkSuite(file_term, search)
            bench.benchmark_controller(iterations)


        for vectorizer in ['count']:
            for transformer in [None,'normal','max','tfidf']:
                for stemmer in ['porter','snowball','lemma',None]:
                    if vectorizer in exclude or stemmer in exclude or transformer in exclude:
                        continue
                    else:
                        __run_search(self.file_term,self.iterations,stemmer,vectorizer,transformer)

    def live_job_processing(self,directory,model=None):
        model = os.path.join(os.getcwd(),self.file_term,'Models','model_files',model)
        """ Sorts job descriptions generated during actual use of the program"""
        model = load(model)
        model.apply_stemming = True if model.stemmer != "No Stemmer" else False
        try:
            live_data = pd.read_sql("SELECT unique_id,job_title,description from unsorted",self.database)
            with self.database:
                cur = self.database.cursor()
                for i,data in live_data.iterrows():
                    live_text = data[1]+'\n'+data[2]
                    label = model.predict(live_text)
                    cur.execute("INSERT INTO results VALUES (?,?,?,?)",(data[0],label,data[1],data[2]))
                    cur.execute("DELETE FROM unsorted WHERE unique_id = ?",(data[0]))
        except Exception as e:
            print(e)


    def get_best_model_configs(self):
        pass

    def tune(self):
        active_models = ['LinearSVC',
                          'LogisticRegressionCV',
                          'LogisticRegression',
                          'Perceptron',
                          'RidgeClassifier',
                          'SGDClassifier']
        self.best_models = {}
        with self.database:
            cur = self.database.cursor()
            for model in active_models:
                a = cur.execute("SELECT MAX(accuracy),unique_id from model_performance_results WHERE model = ?",(model,))
                self.best_models[model] = list(a)[0]
        print(self.best_models)
        s = ClassificationHandler(self.file_term,self.database,'snowball','count',None)
        bench = BenchmarkSuite(self.file_term, s)
        bench.hyperparameter_tuning('LogisticRegression')
        # TODO add model tuning



if __name__ == '__main__':
    import multiprocessing as mp
    from tqdm import tqdm



    clf = ClassificationInterface('Entry Level Computer Programmer',150)
    clf.train_models()












