# coding=utf-8
import re
import string
import nltk

nltk.data.path.append('./nltk_data')

######################## TWEET TOKENIZATION
from nltk.tokenize import RegexpTokenizer

reg_words = r"(?x)"
reg_words += r"(?:[:=;] [oO\-]? [D\)\]\(\]/\\OpP])"  # Smileys
reg_words += r"| <[^>]+>"  # HTML tags
reg_words += r"| (?:\#+[\w_]+[\w\'_\-]*[\w_]+)"  # hashtags
reg_words += r"| (?:@[\w_]+)"  # @mentions
reg_words += r"| \http[s]?(?:[a-z]|[0-9]|[$-_@.&…+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+"  # url
reg_words += r"| (?:(?:\d+,?)+(?:\.?\d+)?)"  # numbers with different variants of format
reg_words += r"| \w'"  # contractions d', l', ...
reg_words += r"| \w+"  # plain words
reg_words += r"| [^\w\s]"  # punctuations
FrenchTweetTokenizer = RegexpTokenizer(reg_words)

from nltk.tokenize import TweetTokenizer

EnglishTweetTokenizer = TweetTokenizer()

######################## STOPWORDS
from nltk.corpus import stopwords

FrenchStopwords = stopwords.words('french')
EnglishStopwords = stopwords.words('english')
excludepunctuation = list(set(string.punctuation))
excludepunctuation.append("rt")
excludepunctuation.append("...")
excludepunctuation.append("…")
excludepunctuation.append("..")
excludepunctuation.append("’")
excludepunctuation.append(". . .")
excludepunctuation.append("�")
excludepunctuation.append("�")
excludepunctuation.append("“")
excludepunctuation.append("_")
excludepunctuation.append("_")
excludepunctuation.append("\ufffd")
excludepunctuation = [i.decode("utf-8") for i in excludepunctuation]

######################## REMOVE URL
URLpattern = re.compile("http[s]?(?:[a-z]|[0-9]|[$-_@.&…+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+")


def removeURL(x):
    return (re.sub(URLpattern, "", x))


######################## STEMMING
FrenchStemmer = nltk.stem.SnowballStemmer('french')
EnglishStemmer = nltk.stem.SnowballStemmer('english')

######################## LEMMATIZING
EnglishLemmatizer = nltk.stem.WordNetLemmatizer()
from pattern.fr import split, parse


def FrenchLemmatizer(myword):
    return (split(parse(myword, lemmata=True))[0].words[-1].lemma)


# ######################## POS TAGGING - NLTK
# from nltk.tag.stanford import StanfordPOSTagger
# #warning: only works with version 2015-04-20
# JAR_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
# French_MODEL_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/models/french.tagger'
# FrenchPostagger = StanfordPOSTagger(French_MODEL_PATH, JAR_PATH, encoding='utf8')
# FrenchTagSelection = ['A','ADV','ET','I','NC', 'V']
#
# English_MODEL_PATH = 'D:/Users/acombess/nltk/stanford-postagger-full-2015-04-20/models/english-left3words-distsim.tagger'
# EnglishPostagger = StanfordPOSTagger(English_MODEL_PATH, JAR_PATH, encoding='utf8')
# EnglishTagSelection = ['FW','JJ','JJR','JJS','MD','NN','NNP','NNPS','NNS',
#                        'RB','RBR','RBS','UH','VB','VBD','VBG','VBN','VBP','VBZ']

######################## POS TAGGING - PATTERN
TagSelection = [u"FW", u"JJ", u"JJR", u"JJS", u"NN", u"NNS", u"NNP", u"NNPS", u"RB", u"RBR", u"RBS", u"RP", u"UH",
                u"VB", u"VBZ", u"VBP", u"VBD", u"VBN", u"VBG"]
from pattern.fr import tag as FrenchTag
from pattern.en import tag as EnglishTag


def tweet_to_words(tweet, query_filter, lang="en", stopwords=True,
                   POStagfilter=True, stemming=False, lemmatization=True):
    if lang == "fr":
        words = FrenchTweetTokenizer.tokenize(removeURL(
            tweet.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore").lower().replace(
                query_filter.decode("utf-8", errors="ignore").lower(), "")))
        words = [x for x in words if x not in excludepunctuation]
        if stopwords:
            words = [x for x in words if x not in FrenchStopwords]
        if POStagfilter:
            tags = [FrenchTag(word)[-1] for word in words]
            words = [x[0] for x in tags if x[1] in TagSelection]
        if stemming: words = [FrenchStemmer.stem(x) for x in words]
        if lemmatization: words = [FrenchLemmatizer(x) for x in words]

    if lang == "en":
        words = EnglishTweetTokenizer.tokenize(removeURL(
            tweet.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore").lower().replace(
                query_filter.decode("utf-8", errors="ignore").lower(), "")))
        words = [x for x in words if x not in excludepunctuation]
        if stopwords:
            words = [x for x in words if x not in EnglishStopwords]
        if POStagfilter:
            tags = [EnglishTag(word)[-1] for word in words]
            words = [x[0] for x in tags if x[1] in TagSelection]
        if stemming: words = [EnglishStemmer.stem(x) for x in words]
        if lemmatization: words = [EnglishLemmatizer.lemmatize(x) for x in words]

    return(words)
