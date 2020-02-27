
from sklearn.feature_extraction.text import HashingVectorizer,CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV


class HashVectPipe:
    parameters ={'clf__alpha': (1.0000000000000001e-05, 9.9999999999999995e-07),
     'clf__max_iter': (10, 50, 80),
     'clf__penalty': ('l2', 'elasticnet'),
     'tfidf__use_idf': (True, False),
     'vect__max_df': (0.5, 0.75, 1.0),
     'vect__max_features': (None, 10,20,50, 100, 500)}

    def __init__(self,model,tokenizer=None,):

        self.vectorizer = HashingVectorizer
        self.ML_model = model
        self.tokenizer = tokenizer

    def using_tfid_transform(self, model_args=None,parameters=None):
        if parameters is None:
            parameters = HashVectPipe.parameters
        if model_args is None:
            model_args = {}
        transformer = TfidfTransformer
        pipe = Pipeline([('vect',self.vectorizer(tokenizer=self.tokenizer())),
                         ('tfidf',transformer()),
                         ('clf',self.ML_model())])
        return GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1)


class CountVectPipe:

    def __init__(self,model,tokenizer=None,):
        self.vectorizer = CountVectorizer
        self.ML_model = model
        self.tokenizer = tokenizer

    def __call__(self, parameters=None):
        if parameters is None:
            parameters = HashVectPipe.parameters
        transformer = TfidfTransformer

        pipe =  Pipeline([('vect',self.vectorizer(tokenizer=self.tokenizer())),
                         ('tfidf',transformer()),
                         ('clf',self.ML_model())])
        return GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1)