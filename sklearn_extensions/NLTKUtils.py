import nltk.data
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
import re


def create_tokens(text):

    to_append = []
    stop_word_regex = re.compile(
        r"((\b| )(for|is|a|the|an|as|to|and|with|in|inc|eg|etc|n/a|that|be|[A-Za-z0-9]{1})([^A-Za-z0-9]|\b))+")
    text = text.lower().strip()
    ex = re.compile(r'(\b| )?([0-9])((-)([0-9])|\+) years?')
    experience = re.findall(ex,text)
    gpa = re.findall(r'(\b| )([0-9]\.[0-9])',text)
    if experience:
        for exp in experience:
            base = int(exp[1])
            if exp[2] == '+':
                for i in range(base,base+3):
                    to_append.append(f'{i} years')
            elif exp[3] == '-':
                for i in range(int(exp[1]),int(exp[4])+1):
                    to_append.append(f'{i} years')
    if gpa:
        for g in gpa:
            to_append.append(g[1])

    text = re.sub(ex,' ',text)
    text = re.sub(r'(\b| )([0-9]\.[0-9])',' ',text)
    text = re.sub(stop_word_regex, ' ', text)


    text = re.sub(r'(http(s)?://(www\.)?|www\.)([a-zA-Z0-9]+(/([a-zA-Z0-9]+(\.[a-zA-Z]{2,4})?)?|\.[a-zA-Z]{2,4}[/]?))+',
                  '', text)
    text = re.sub('%', ' percent', text)
    text = re.sub(r'[^A-Za-z0-9]+',' ',text)
    #text = re.sub(r'[()\n.?!\'\",:;]', '', text)
    #text = re.sub(r'[\\/\-|_]', ' ', text)

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
        return [self.wnl.lemmatize(t,LemmaTokenizer.tag_map[tag[0]]) for t,tag in pos_tag(create_tokens(doc))]

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