from sklearn.model_selection import train_test_split
from sklearn_extensions.benchmarks import *
from sklearn_extensions.NLTKUtils import *
from sklearn_extensions.featurization import *
from sklearn_extensions.extended_pipeline import PipelineComponents
from joblib import load


class ClassificationHandler:

    job_label_associations = {'Good Jobs':'Good', 'Bad Jobs':'Bad', 'Neutral Jobs':'Bad', 'Ideal Jobs':'Good'}

    def __init__(self,search_term : str,stemmer : str = None,vectorizer='count',transform=False,training=True):
        self.search_term = search_term
        self.jobs = []
        self.goodjobs_encoded = {}
        self.badjobs_encoded = {}
        self.dataset = defaultdict(list)
        self.stemmer = stemmer

        # live sorting uses pickled models , so no customization of text processing is allowed
        if training:
            self._jobdesc_preprocessing()
            self.vectorizer = vectorizer
            self.transform = transform

    def _process_text(self):
        pass

    def _jobdesc_preprocessing(self):
        '''Processes the text files to remove punctuation, noise (i.e url's), and case from the text
         and assignes the result to a pandas dataframe containing the label and content'''

        stemmer = PipelineComponents.stemmers[self.stemmer]
        job_cat_data = {}
        paths = {}
        for subfolder in ['Good Jobs', 'Bad Jobs', 'Neutral Jobs', 'Ideal Jobs']:
            paths[subfolder] = os.path.join(os.getcwd(), self.search_term, 'Train', subfolder)
            job_cat_data[subfolder] = os.scandir(os.path.join(os.getcwd(), self.search_term, 'Train', subfolder))
        for joblabel,data in job_cat_data.items():
            for job in data:
                with open(os.path.join(paths[joblabel],job.name), 'r') as jobdesc:
                    raw = jobdesc.readlines()[7:]
                    formatted_data = " ".join(raw)
                self.dataset['content'].append(stemmer(formatted_data))
                self.dataset['label'].append(ClassificationHandler.job_label_associations[joblabel])
        self.dataset = pd.DataFrame(self.dataset)

    def live_job_processing(self,directory,model=None):
        model = os.path.join(os.getcwd(),self.search_term,'Models','model_files','snowball_count_normal_SGDClassifier')
        """ Sorts job descriptions generated during actual use of the program"""
        model = load(model)
        model.apply_stemming = True
        try:
            with open(directory,'r') as job:
                content = [job.read()]
        except FileNotFoundError:
            return
        label = model.predict(content)
        return label

    def _split_dataset(self):
        """ Splits the presorted job data for model training"""
        train,test = train_test_split(self.dataset,test_size=0.3,stratify = self.dataset.label,shuffle=True)
        y_train,y_test = train.label.values,test.label.values
        X_train,X_test = train.content.values,test.content.values

        self.X_train,self.X_test = X_train,X_test
        self.y_train,self.y_test = y_train,y_test

    def model_data(self,*argss):
        self._split_dataset()
        bench = BenchmarkSuite(self.search_term,self.X_train,self.X_test,self.y_train,self.y_test,stemmer=self.stemmer,vectorizer=self.vectorizer,transform=self.transform)
        bench.show_results(silent=False,plot=False)
        return 'None'
    def tune_model(self,model : str):
        self._split_dataset()
        bench = BenchmarkSuite(self.search_term, self.X_train, self.X_test, self.y_train, self.y_test,
                               stemmer=self.stemmer, vectorizer=self.vectorizer, transform=self.transform)
        bench.hyperparameter_tuning(model)
        return 'done'

if __name__ == '__main__':
    import multiprocessing as mp
    from tqdm import tqdm
    def tune(file_term,model):
        search = ClassificationHandler(file_term, vectorizer='count', stemmer='snowball', transform=True)
        search.tune_model(model)


    @comparison_decorator
    def searchf(file_term,iterations,stemmer,vectorizer,transformer):
        search = ClassificationHandler(file_term, vectorizer= vectorizer,stemmer=stemmer,transform=transform)
        for _ in tqdm(range(iterations)):
            search.model_data()


    for vectorizer in ['count','hashing']:
        for transform in [None,'normal','minmax','tfidf','normal']:
            for stemmer in [None,'porter','snowball','lemma']:
                searchf('Chemical Engineer',150,stemmer,vectorizer,transform)











