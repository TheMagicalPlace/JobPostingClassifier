import nltk.data
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import defaultdict

class LemmaTokenizer:
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t,LemmaTokenizer.tag_map[tag[0]]) for t,tag in pos_tag(doc)]

class StemTokenizer:
    def __init__(self):
        self.wnl = PorterStemmer()
    def __call__(self, doc):
        return [self.wnl.stem(t) for t in word_tokenize(doc)]