# coding=utf-8
import re
import string
import nltk
import pattern.fr
import pattern.es
import pattern.en
import pattern.de
import pattern.it
import pattern.nl


######################## TWEET TOKENIZATION

FrenchSentenceTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
EnglishSentenceTokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
SpanishSentenceTokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
GermanSentenceTokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
ItalianSentenceTokenizer = nltk.data.load('tokenizers/punkt/italian.pickle')
DutchSentenceTokenizer = nltk.data.load('tokenizers/punkt/dutch.pickle')

###### !!!!! RegexpTokenizer and TweetTokenizer from NLTK have problems with emoticons,
###### !!!! so have been replace by TreeBankWordTokenizer
# from nltk.tokenize import RegexpTokenizer
# reg_words = r"(?x)"
# reg_words += r"(?:[:=;] [oO\-]? [D\)\]\(\]/\\OpP])"  # Smileys
# reg_words += r"| <[^>]+>"   # HTML tags
# reg_words += r"| (?:\#+[\w_]+[\w\'_\-]*[\w_]+)"  # hashtags
# reg_words += r"| (?:@[\w_]+)"  # @mentions
# reg_words += r"| \http[s]?(?:[a-z]|[0-9]|[$-_@.&…+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"  # url
# reg_words += r"| (?:(?:\d+,?)+(?:\.?\d+)?)"  # numbers with different variants of format
# reg_words += r"| \w'"  # contractions d', l', ...
# reg_words += r"| \w+"  # plain words
# reg_words += r"| [^\w\s]"  # punctuations
# FrenchTweetTokenizer = RegexpTokenizer(reg_words)
# SpanishTweetTokenizer = RegexpTokenizer(reg_words)
# GermanTweetTokenizer = RegexpTokenizer(reg_words)
# ItalianTweetTokenizer = RegexpTokenizer(reg_words)
# DutchTweetTokenizer = RegexpTokenizer(reg_words)
#
# from nltk.tokenize import TweetTokenizer
# EnglishTweetTokenizer = TweetTokenizer()

from nltk.tokenize import TreebankWordTokenizer
EnglishTweetTokenizer = TreebankWordTokenizer()
FrenchTweetTokenizer = TreebankWordTokenizer()
SpanishTweetTokenizer = TreebankWordTokenizer()
GermanTweetTokenizer = TreebankWordTokenizer()
ItalianTweetTokenizer = TreebankWordTokenizer()
DutchTweetTokenizer = TreebankWordTokenizer()


######################## STOPWORDS
from nltk.corpus import stopwords

FrenchStopwords = list(set(stopwords.words('french')))
FrenchStopwords.extend([u'rt',u'gt',u'amp',u'être',u'avoir'])
EnglishStopwords = list(set(stopwords.words('english')))
EnglishStopwords.extend([u'rt',u'gt',u'amp'])
SpanishStopwords = list(set(stopwords.words('spanish')))
SpanishStopwords.extend([u'rt',u'gt',u'amp'])
GermanStopwords = list(set(stopwords.words('german')))
GermanStopwords.extend([u'rt',u'gt',u'amp'])
ItalianStopwords = list(set(stopwords.words('italian')))
ItalianStopwords.extend([u'rt',u'gt',u'amp'])
DutchStopwords = list(set(stopwords.words('dutch')))
DutchStopwords.extend([u'rt',u'gt',u'amp'])

excludepunctuation = list(set(string.punctuation))
excludepunctuation.extend(["`",u'`','`','`',"'",'`','`','+',"'",'`',"'",'\\\\','`',"’","'","...","`","…","..","’",". . .","�","“","_","\ufffd","—","'"])
excludepunctuation = {i.decode("utf-8") for i in excludepunctuation}        

######################## REMOVE URL
URLpattern = re.compile("http[s]?(?:[a-z]|[0-9]|[$-_@.&…+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+")

def removeURL(x,string_rep=u""):
    return(re.sub(URLpattern, string_rep, x))


######################## STEMMING
FrenchStemmer = nltk.stem.SnowballStemmer('french')
EnglishStemmer = nltk.stem.SnowballStemmer('english')
SpanishStemmer = nltk.stem.SnowballStemmer('spanish')
GermanStemmer = nltk.stem.SnowballStemmer('german')
ItalianStemmer = nltk.stem.SnowballStemmer('italian')
DutchStemmer = nltk.stem.SnowballStemmer('dutch')

######################## LEMMATIZING
def EnglishLemmatizer(myword):
    return(nltk.stem.WordNetLemmatizer().lemmatize(myword))

def FrenchLemmatizer(myword):
    return(pattern.fr.split(pattern.fr.parse(myword, lemmata=True))[0].words[-1].lemma)

def SpanishLemmatizer(myword):
    return(pattern.es.split(pattern.es.parse(myword, lemmata=True))[0].words[-1].lemma)

def GermanLemmatizer(myword):
    return(pattern.de.split(pattern.de.parse(myword, lemmata=True))[0].words[-1].lemma)

def ItalianLemmatizer(myword):
    return(pattern.it.split(pattern.it.parse(myword, lemmata=True))[0].words[-1].lemma)

def DutchLemmatizer(myword):
    return(pattern.nl.split(pattern.nl.parse(myword, lemmata=True))[0].words[-1].lemma)

# ######################## POS TAGGING - NLTK - TOO SLOW
# from nltk.tag.stanford import StanfordPOSTagger
# #warning: only works with version 2015-04-20
# JAR_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
# French_MODEL_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/models/french.tagger'
# FrenchPostagger = StanfordPOSTagger(French_MODEL_PATH, JAR_PATH, encoding='utf8')
#
# English_MODEL_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/models/english-left3words-distsim.tagger'
# EnglishPostagger = StanfordPOSTagger(English_MODEL_PATH, JAR_PATH, encoding='utf8')


######################## POS TAGGING - PATTERN
TagSelection = [u"FW", u"JJ", u"JJR", u"JJS", u"NN", u"NNS", u"NNP", u"NNPS", u"RB", u"RBR", u"RBS", u"RP", u"UH",
                u"VB", u"VBZ", u"VBP", u"VBD", u"VBN", u"VBG"]
from pattern.fr import tag as FrenchTag
from pattern.en import tag as EnglishTag
from pattern.es import tag as SpanishTag
from pattern.de import tag as GermanTag
from pattern.it import tag as ItalianTag
from pattern.nl import tag as DutchTag


text_processor = {
    "en":{
        "SentenceTokenizer": EnglishSentenceTokenizer,
        "WordTokenizer": EnglishTweetTokenizer,
        "Stopwords": EnglishStopwords,
        "POSTagger": EnglishTag,
        "Stemmer": EnglishStemmer,
        "Lemmatizer": EnglishLemmatizer,
    },
    "fr":{
        "SentenceTokenizer": FrenchSentenceTokenizer,
        "WordTokenizer": FrenchTweetTokenizer,
        "Stopwords": FrenchStopwords,
        "POSTagger": FrenchTag,
        "Stemmer": FrenchStemmer,
        "Lemmatizer": FrenchLemmatizer,
    },
    "es":{
        "SentenceTokenizer": SpanishSentenceTokenizer,
        "WordTokenizer": SpanishTweetTokenizer,
        "Stopwords": SpanishStopwords,
        "POSTagger": SpanishTag,
        "Stemmer": SpanishStemmer,
        "Lemmatizer": FrenchLemmatizer,
    },
    "it":{
        "SentenceTokenizer": ItalianSentenceTokenizer,
        "WordTokenizer": ItalianTweetTokenizer,
        "Stopwords": ItalianStopwords,
        "POSTagger": ItalianTag,
        "Stemmer": ItalianStemmer,
        "Lemmatizer": ItalianLemmatizer,
    },
    "de":{
        "SentenceTokenizer": GermanSentenceTokenizer,
        "WordTokenizer": GermanTweetTokenizer,
        "Stopwords": GermanStopwords,
        "POSTagger": GermanTag,
        "Stemmer": GermanStemmer,
        "Lemmatizer": GermanLemmatizer,
    },
    "nl":{
        "SentenceTokenizer": DutchSentenceTokenizer,
        "WordTokenizer": DutchTweetTokenizer,
        "Stopwords": DutchStopwords,
        "POSTagger": DutchTag,
        "Stemmer": DutchStemmer,
        "Lemmatizer": DutchLemmatizer,
    },
}

def flatten_all(iterable):
    for elem in iterable:
        if not isinstance(elem, list):
            yield elem
        else:
            for x in flatten_all(elem):
                yield x

######################## TEXT PROCESSING FUNCTIONS


def doc_to_words(doc, query_filter="", lang="fr", date="", stopwords=True, excludepunct=True,
                 POStagfilter=True, stemming=False, lemmatization=True, sentence_token=False,
                 correct_dic=None):
    if sentence_token:
        sentences = text_processor[lang]["SentenceTokenizer"].tokenize(removeURL(
            doc.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore").lower().replace(
                query_filter.lower(), "")))
        words = [text_processor[lang]["WordTokenizer"].tokenize(sentence) for sentence in sentences]
        if correct_dic is not None:
            words = [flatten_all([correct_dic.get(item, item) for item in sentence]) for sentence in words]
        if excludepunct:
            words = [[x for x in s if x not in excludepunctuation] for s in words]
        if stopwords:
            words = [[x for x in s if x not in text_processor[lang]["Stopwords"]] for s in words]
        if POStagfilter:
            tags = [[text_processor[lang]["POSTagger"](word)[-1] for word in s] for s in words]
            words = [[x[0] for x in t if x[1] in TagSelection] for t in tags]
        if stemming: words = [[text_processor[lang]["Stemmer"].stem(x) for x in s] for s in words]
        if lemmatization:
            words = [[text_processor[lang]["Lemmatizer"](x) for x in s] for s in words]

    else:
        words =  text_processor[lang]["WordTokenizer"].tokenize(removeURL(
            doc.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore").lower().replace(
                query_filter.lower(), "")))
        if correct_dic is not None:
            words = flatten_all([correct_dic.get(item, item) for item in words])
        if excludepunct:
            words = [x for x in words if x not in excludepunctuation]
        if stopwords:
            words = [x for x in words if x not in text_processor[lang]["Stopwords"]]
        if POStagfilter:
            tags = [text_processor[lang]["POSTagger"](word)[-1] for word in words]
            words = [x[0] for x in tags if x[1] in TagSelection]
        if stemming: words = [text_processor[lang]["Stemmer"].stem(x) for x in words]
        if lemmatization: words = [text_processor[lang]["Lemmatizer"](x) for x in words]

    return(filter(None, words))



def ratio_upper_case(doc):
    doc=doc.replace(" ","")
    return(float(sum(c.isupper() for c in doc))/float(len(doc)))

def ratio_punctuation(doc):
    doc=doc.replace(" ","")
    return(float(sum(c in excludepunctuation for c in doc))/float(len(doc)))

def ratio_correction(doc, correct_dic, lang="fr"):
    doc_token = text_processor[lang]["WordTokenizer"].tokenize(removeURL(
        doc.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore").lower()))
    words_to_correct = set(correct_dic.keys())
    nb_words_to_correct = sum([1 for d in doc_token if d in words_to_correct])
    return(float(nb_words_to_correct)/float(len(doc_token)))

def ratio_number(doc):
    doc=doc.replace(" ","")
    return(float(sum(c.isnumeric() for c in doc))/float(len(doc)))

def ratio_emoticon(doc):
    len_without_emoticon = len(doc.encode("cp500",errors="ignore").decode("cp500",errors="ignore").replace(" ",""))
    return(1.-float(len_without_emoticon)/float(len(doc.replace(" ",""))))

