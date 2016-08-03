# coding=utf-8

import ast
import json
import os
import time

import tweepy
from progressbar import Bar, ETA, Percentage, ProgressBar
from numpy import random

import sys
sys.path.append('./CommuniTweet/')
import CommuniTweet.textprocessing64 as txtpro

#sys.path.append('C:/CommuniTweet/CommuniTweet')
#import textprocessing64 as txtpro

consumer_key = ast.literal_eval(os.environ.get('CONSUMER_KEY'))
consumer_secret = ast.literal_eval(os.environ.get('CONSUMER_SECRET'))
access_token = ast.literal_eval(os.environ.get('ACCESS_TOKEN'))
access_secret = ast.literal_eval(os.environ.get('ACCESS_SECRET'))

# origin=['alteralec','giftguru','imachraoui','thibaut','laura','thibaut2']

class TwitterApiUtil():
    def __init__(self, ):
        self.num_api = len(consumer_key)
        self.auth = [None] * self.num_api
        self.apis = [None] * self.num_api
        for i in range(self.num_api):
            self.auth[i] = tweepy.OAuthHandler(consumer_key[i], consumer_secret[i])
            self.auth[i].set_access_token(access_token[i], access_secret[i])
            self.apis[i] = tweepy.API(self.auth[i])
        self.current_api_index = 0
        self.rate_limit_status = [x.rate_limit_status() for x in self.apis]
        self.rate_limit_app = [x["resources"]["statuses"]["/statuses/user_timeline"] for x in self.rate_limit_status]
        self.rate_limit_counter = [x["remaining"] for x in self.rate_limit_app][self.current_api_index]

    def get_apis(self):
        return (self.apis)

    def search_limit(self, api):
        try:
            return (api.rate_limit_status()["resources"]["search"]["/search/tweets"])
        except tweepy.TweepError:
            time.sleep(15 * 60)
            print("sleeping for 15 minutes")

    def search_limit_all(self):
        try:
            print([(i, self.search_limit(self.apis[i])["remaining"]) for i in range(self.num_api)])
        except tweepy.TweepError:
            time.sleep(15 * 60)
            print("sleeping for 15 minutes")

    def time_search_limit(self, api):
        try:
            return (self.search_limit(api)["reset"] - time.time())
        except tweepy.TweepError:
            time.sleep(15 * 60)
            print("sleeping for 15 minutes")

    def statuses_timeline_limit(self, api):
        try:
            return (api.rate_limit_status()["resources"]["statuses"]["/statuses/user_timeline"])
        except tweepy.TweepError:
            time.sleep(15 * 60)
            print("sleeping for 15 minutes")

    def statuses_timeline_limit_all(self):
        try:
            print([(i, self.statuses_timeline_limit(self.apis[i])["remaining"]) for i in range(self.num_api)])
        except tweepy.TweepError:
            time.sleep(15 * 60)
            print("sleeping for 15 minutes")

    def get_random_api(self):
        self.current_api_index = random.randint(0, self.num_api - 1)
        return (self.apis[self.current_api_index])

    def get_api_search(self):
        apis_status = [self.search_limit(self.apis[i]) for i in range(0, self.num_api)]
        apis_remaining = [x["remaining"] for x in apis_status]
        apis_reset = [x["reset"] - time.time() for x in apis_status]
        current_remaining = apis_remaining[self.current_api_index]
        while current_remaining < 80:
            apis_status = [self.search_limit(self.apis[i]) for i in range(0, self.num_api)]
            apis_remaining = [x["remaining"] for x in apis_status]
            apis_reset = [x["reset"] - time.time() for x in apis_status]
            current_remaining = apis_remaining[self.current_api_index]
            if max(apis_remaining) < 80:
                time.sleep(abs(min(apis_reset)))
                self.current_api_index = apis_reset.index(min(apis_reset))
            else:
                self.current_api_index = apis_remaining.index(max(apis_remaining))
        return (self.apis[self.current_api_index])

    def get_api_usertimeline(self):
        self.rate_limit_counter -= 1
        while self.rate_limit_counter < 1:
            self.rate_limit_status = [x.rate_limit_status() for x in self.apis]
            self.rate_limit_app = [x["resources"]["statuses"]["/statuses/user_timeline"] for x in
                                   self.rate_limit_status]
            self.rate_limit_counter = [x["remaining"] for x in self.rate_limit_app][self.current_api_index]
            apis_reset = [x["reset"] - time.time() for x in self.rate_limit_app]
            print "self.rate_limit_app",self.rate_limit_app            
            print "x:",x
            print "apis_reset",apis_reset
            if max([x["remaining"] for x in self.rate_limit_app]) < 1:
                time.sleep(min(apis_reset))
                print("sleeping for " + str(min(apis_reset)) + " seconds")
                self.current_api_index = apis_reset.index(min(apis_reset))
            else:
                self.current_api_index = [x["remaining"] for x in self.rate_limit_app].index(
                    max([x["remaining"] for x in self.rate_limit_app]))
        # print(self.rate_limit_counter, self.current_api_index)
        return (self.apis[self.current_api_index])

    def printjson(self, x):
        print(json.dumps(x._json))

    def storejson(self, x, outfile):
        with open(outfile, 'w') as f:
            for i in x:
                json.dump(i._json, f)
                f.write('\n')

    def tw_search(self, query, lang='en', n_items_search=1000):
        jsoncollection = []
        widgets = [Percentage(), ' ', Bar(), ' ', ETA()]
        time.sleep(1)
        print("Searching Twitter for your query...")
        pbar = ProgressBar(widgets=widgets, maxval=n_items_search).start()
        i = 0
        for tweet in tweepy.Cursor(self.get_api_search().search, q=query, lang=lang).items(n_items_search):
            jsoncollection.append(json.dumps(tweet._json))
            i += 1
            pbar.update(i)
        pbar.finish()
        return (jsoncollection)

    def tw_users_from_search(self, query, lang="en", n_items_search=1000):
        jsoncollection = self.tw_search(query, lang, n_items_search)
        list_users = list(set([json.loads(x)["user"]["id_str"] for x in jsoncollection]))
        return (list_users)

    def get_tweets_from_users(self, user_id_list, n_tweets_per_user=100, lang="en"):
        tw_text = []
        tw_name = []
        tw_dict = []
        new_tweets = []
        time.sleep(1)
        print("Downloading tweets from users...")
        pbar = ProgressBar(widgets=[Percentage(), ' ', Bar(), ' ', ETA()]).start()
        for user_id in pbar(user_id_list):
            try:
                new_tweets = self.get_api_usertimeline().user_timeline(user_id=str(user_id),
                                                                       count=n_tweets_per_user, include_rts=True)
            except tweepy.TweepError:
                if tweepy.TweepError is "[{u'message': u'Over capacity', u'code': 130}]":
                    print(tweepy.TweepError)
                    time.sleep(2 * 60)
            new_text = [x.text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore") for x in new_tweets if
                        x.lang == lang]
            new_name = str(new_tweets[0].user.screen_name.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))
            new_dict = {"screen_name": new_name, "text": new_text}
            tw_text.append(new_text)
            tw_name.append(new_name)
            tw_dict.append(new_dict)
        return (tw_dict)

    def get_tweets_from_search(self, query, lang="en", date="", n_items_search=1000, n_tweets_per_user=100):
        user_id_list = self.tw_users_from_search(query=query, lang=lang, n_items_search=n_items_search)
        if user_id_list != []:
            tw_dict = self.get_tweets_from_users(user_id_list=user_id_list, n_tweets_per_user=n_tweets_per_user, lang=lang)
            final_dict = {"query": query, "language":lang, "date":date, "users": tw_dict}
            return (final_dict)
        else:
            return {"users":[]}

    def dict_text_processing(self, d, query_filter, lang="en",date="", stopwords=True, excludepunct=True, POStagfilter=True, stemming=False,
                             lemmatization=True):
        time.sleep(1)
        print("Processing tweets' text...")
        pbar = ProgressBar(widgets=[Percentage(), ' ', Bar(), ' ', ETA()])
        for dict in pbar(d["users"]):
            dict["text"] = txtpro.doc_to_words("\n".join(dict["text"]), query_filter=query_filter,
                                                 lang=lang, date=date, stopwords=stopwords, excludepunct=excludepunct, POStagfilter=POStagfilter,
                                                 stemming=stemming, lemmatization=lemmatization)
        return (d)

    def get_tweets_from_search_cleaned(self, query, lang="en", date="", n_items_search=1000, n_tweets_per_user=100, stopwords=True, excludepunct=True, POStagfilter=True, stemming=False, lemmatization=True):
        if self.get_tweets_from_search(query, lang, date, n_items_search, n_tweets_per_user) != {"users":[]}:        
            return (self.dict_text_processing(d=self.get_tweets_from_search(query, lang, date, n_items_search, n_tweets_per_user),
                                          query_filter=query, lang=lang, date=date, stopwords=stopwords,excludepunct=excludepunct,
                                          POStagfilter=POStagfilter, stemming=stemming, lemmatization=lemmatization))
        else:
            return {"users":[]}
