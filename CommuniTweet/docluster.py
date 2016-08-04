# coding=utf-8

from time import time

from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

word_filters = [u"n't", u"'s",u"\ud83d",u"\ud83c",u"\ude02",u"\ude4c",u"\ufe0f",u"\ude2d",u"\ude1c",u"\ude0f",u"\udf77",
                u"\ude18",u"\udffd",u"\u2018",u'\ud83d',u'\ud83c',u'_',u"'m",u'\uddf8',u'\ude0d',u'\uddfa',u"'re",u'_',
                u'\udd25',u"'ve",u'''n't''',u'\udc80',u'\ude44',u'\udf89',u'\ude0a',u'\ud83e', u'\ude29', u'\ude01',
                u'\udffe',u'\udffc',u'\udfb6',u'\udc95',u'\udffb',u'\udc95',u'\udc40',u'\udc4c',u'\ude04',u'\ude09',
                u'\udc4f',u'\ude07',u'\ude3b',u'\udcaf',u'\u2014',u'r',u'j',u'\udd14',u'b',u'\u2022',u'v',u'http',
                u"\ude43",u"\ude4f",u"\ub354\uc1fc",u'\ub354\uc1fc',u'\udc96',u'\udc4d',u'\ude4f',u'\ude43',u'c',u'h',
                u"\udd07",u"\udc9c",u"\udcf7",u"\udc96",u"\ude48",u"http",u"\ude33",u"\udc8b",u"\udc97",u"\udf27",u"\ude4f",
                u"\ude96",u"\ude05",u"\udf39",u"\udf27",u"\udc99"]

def cluster_tweets(tweetdic, n_clusters=4, n_word_out=100, max_df=0.95, min_df=0.05, SVD_components=500, n_iter=50,
                   random_state=42):
    t0 = time()
    vectorizer = TfidfVectorizer(analyzer=lambda x: x, tokenizer=lambda x: x, max_df=max_df, min_df=min_df,
                                 encoding="utf-8", decode_error="ignore", strip_accents="unicode")
    X = vectorizer.fit_transform([t["text"] for t in tweetdic["users"]])
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % X.shape)

    svd = TruncatedSVD(n_components=SVD_components, n_iter=n_iter, random_state=random_state)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)
    X = lsa.fit_transform(X)
    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(int(explained_variance * 100)))

    km = KMeans(n_clusters=n_clusters, init='k-means++', n_jobs=1, n_init=n_iter, random_state=random_state)
    print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X)

    print("Top terms per cluster:")
    original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    community_list = []
    for i in range(n_clusters):
        community_dic = {
            "screen_names": [x["screen_name"] for j, x in enumerate(tweetdic["users"]) if km.labels_.tolist()[j] == i],
            "words": [{"text": terms[order_centroids[i, j]],
                       "weight": original_space_centroids[i, order_centroids[i, j]]}
                      for j in range(n_word_out)
                      if terms[order_centroids[i, j]] not in word_filters]
        }
        community_list.append(community_dic)
        print("Cluster %d: " % (i + 1) + str(len(community_dic["screen_names"])) + " people "
              + str([terms[order_centroids[i, j]] for j in range(50) if terms[order_centroids[i, j]] not in word_filters]))
        # print("Cluster %d: " % i + str([original_space_centroids[i,order_centroids[i,j]] for j in range(10)]))
        
    final_dic = {
        "query": tweetdic["query"],
        "language": str(tweetdic["language"]),
        "date": str(tweetdic["date"]),
        "communities": community_list,
    }

    print("done in %fs" % (time() - t0))
    return(final_dic)
