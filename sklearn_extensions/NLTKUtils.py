import nltk.data
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
import re
import tqdm
from pymagnitude import Magnitude
import numpy as np
import os


# TODO - add number-word equv. to tokenizer, i.e. 1-'one' etc. for experience regex
def create_tokens(text: str):
    """Custom word tokenizer based specifically on cleaning up and tokenizing job postings

    Note: this is meant to parse a single document string only, and should not be made to work directly with
    iterables of any kind
    """
    _ = r'one|two|three|four|five|six|seven|eight|nine|zero'
    num2int = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'zero':0}
    to_append = []
    stop_word_regex = re.compile(
        r"((\b| )(for|is|a|the|an|as|to|and|with|in|inc|eg|etc|n/a|that|be|[A-Za-z0-9]{1})([^A-Za-z0-9]|\b))+")
    text = text.lower().strip()
    ex = re.compile(r'(\b| )?([0-9]|one|two|three|four|five|six|seven|eight|nine|zero)((-)([0-9]+|one|two|three|four|five|six|seven|eight|nine|zero)|\+)? years?')
    experience = re.findall(ex, text)
    gpa = re.findall(r'(\b| )([0-9]\.[0-9])', text)

    # feature engineering, 'X years of experience, X-Y years of experience, X+ years of experience' are all
    # made into custom tokens to better reflect their significance as pertains to job postings
    if experience:
        for exp in experience:
            try:
                base = int(num2int[exp[1]])
            except KeyError:
                base = int(exp[1])
            if exp[2] == '+':
                for i in range(base, base + 3):
                    to_append.append(f'{i} years')
            elif exp[3] == '-':

                try:
                    nu =int(num2int[exp[4]])
                except KeyError:
                    nu = int(exp[4])
                for i in range(base, nu + 1):
                    to_append.append(f'{i} years')

    # same with GPA requirements
    if gpa:
        for g in gpa:
            to_append.append(g[1])

    # removing custom features
    text = re.sub(ex, ' ', text)
    text = re.sub(r'(\b| )([0-9]\.[0-9])', ' ', text)

    # removing stop words
    text = re.sub(stop_word_regex, ' ', text)

    # removing any website links
    text = re.sub(r'(http(s)?://(www\.)?|www\.)([a-zA-Z0-9]+(/([a-zA-Z0-9]+(\.[a-zA-Z]{2,4})?)?|\.[a-zA-Z]{2,4}[/]?))+',
                  '', text)

    # substituting symbol(s) with corresponding words
    text = re.sub('%', ' percent', text)

    # removing any remaining non alpha-numberic characters
    text = re.sub(r'[^A-Za-z0-9]+', ' ', text)

    text = text.strip().split(' ')
    text = [t for t in text if t.strip() != '']
    text += to_append
    return text


class LemmaTokenizer:
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t, LemmaTokenizer.tag_map[tag[0]]) for t, tag in pos_tag(create_tokens(doc))]


class LemmaTokenizerBase:
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in create_tokens(doc)]


class StemTokenizer:
    def __init__(self):
        self.wnl = PorterStemmer()

    def __call__(self, doc):
        return [self.wnl.stem(t) for t in word_tokenize(doc)]


class SnowballTokenizer:
    def __init__(self):
        self.wnl = SnowballStemmer(language='english')

    def __call__(self, doc):
        return [self.wnl.stem(t) for t in create_tokens(doc)]


class GloveStruct:
    """contains glove for use with glove based document processing

    implemented as a class to avoid cluttering global namespace"""
    glove = Magnitude(os.path.join(os.getcwd(), 'sklearn_extensions', 'vectors', 'glove.6B.100d.magnitude'))


class GloveTokenize:
    def __init__(self):
        self.glove = GloveStruct.glove

    def _doc_transform(self, doc):
        return np.average(GloveStruct.glove.query(create_tokens(doc)), axis=0)

    def fit(self, X, y=None):
        res = []
        for doc in X:
            res.append(self._doc_transform(doc))
        return res

    def transform(self, X):
        return self.fit(X)

    def fit_transform(self, X, y=None):
        res = []
        for doc in X:
            res.append(self._doc_transform(doc))
        return res


def avg_glove(df):
    vectors = []
    for t in tqdm(df.content.values):
        vectors.append(np.average(GloveStruct.glove.query(word_tokenize(t)), axis=0))
    return np.array(vectors)


def tfidf_glove(df, idf_dict):
    vectors = []
    for title in tqdm(df.content.values):
        glove_vectors = GloveStruct.glove.query(word_tokenize(title))
        weights = [idf_dict.get(word, 1) for word in word_tokenize(title)]
        vectors.append(np.average(glove_vectors, axis=0, weights=weights))
    return np.array(vectors)
