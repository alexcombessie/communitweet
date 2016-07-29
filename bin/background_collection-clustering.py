# coding=utf-8
# Importing necessary libraries
import os
import sys
from time import time
import datetime

t0 = time()

sys.path.append('./CommuniTweet/')
# Importing custom modules
from CommuniTweet.twscrap import TwitterApiUtil
tw_util = TwitterApiUtil()
import CommuniTweet.mongolab as mlab
import CommuniTweet.docluster as clust

#sys.path.append('C:/CommuniTweet/CommuniTweet')
# Importing custom modules
#from twscrap import TwitterApiUtil
#tw_util = TwitterApiUtil()
#import mongolab as mlab
#import docluster as clust

search = mlab.download_query()
if search["Priority"] == 1:
    query_to_be_processed = search["query"]
    lang = str(search["language"])
    date = str(search["date"])
    print("Priority:1\n")
    print("Processing query:" + query_to_be_processed + " in "+ lang + " of " + date)
    raw_data = tw_util.get_tweets_from_search_cleaned(query_to_be_processed,n_items_search=1000,n_tweets_per_user=100,lang=lang)
    mlab.update_status_collected(query_to_be_processed,lang,date,True) 
    mlab.update_processing_date(query_to_be_processed,lang,date)
    if len(raw_data["users"])<50:
        print("Too few users for your query")
        mlab.update_status_collected(query_to_be_processed,lang,date,"Too few users")
        mlab.update_status_clustered(query_to_be_processed,lang,date,"Too few users")
        mlab.update_priority(query_to_be_processed,lang,date,3)
    else:
        # mlab.upload_twitter_raw(raw_data)
        cluster_data = clust.cluster_tweets(raw_data)
        cluster_data["date"]=date
        cluster_data["language"]=lang
        mlab.upload_twitter_community(cluster_data)
        mlab.update_status_clustered(query_to_be_processed,lang,date,True)
        mlab.update_priority(query_to_be_processed,lang,date,2)
    print("All done in %f minutes!" % ((time() - t0) / 60))
elif search["Priority"] == 2:
    query_to_be_processed = search["query"]
    lang = str(search["language"])
    FormerDate=str(search["date"])
    mlab.uploadToMongolab(query_to_be_processed,lang,2)
    date=str(datetime.datetime.now().date())
    print("Priority:2\n")
    print("Processing query:" + query_to_be_processed + " in "+ lang + " of " + date)
    raw_data = tw_util.get_tweets_from_search_cleaned(query_to_be_processed,n_items_search=1000,n_tweets_per_user=100,lang=lang)
    mlab.update_status_collected(query_to_be_processed,lang,date,True) 
    mlab.update_processing_date(query_to_be_processed,lang,date)
    if len(raw_data["users"])<50:
        print("Too few users for your query")
        mlab.update_status_collected(query_to_be_processed,lang,date,"Too few users")
        mlab.update_status_clustered(query_to_be_processed,lang,date,"Too few users")
        mlab.update_priority(query_to_be_processed,lang,date,3)
        mlab.update_priority(query_to_be_processed,lang,FormerDate,False)
    else:
        # mlab.upload_twitter_raw(raw_data)
        cluster_data = clust.cluster_tweets(raw_data)
        cluster_data["date"]=date
        cluster_data["language"]=lang
        mlab.upload_twitter_community(cluster_data)
        mlab.update_status_clustered(query_to_be_processed,lang,date,True)
        mlab.update_priority(query_to_be_processed,lang,date,2)
        mlab.update_priority(query_to_be_processed,lang,FormerDate,False)
    print("All done in %f minutes!" % ((time() - t0) / 60))   
elif search["Priority"] == 3:
    query_to_be_processed = search["query"]
    lang = str(search["language"])
    FormerDate=str(search["date"])
    date=str(datetime.datetime.now().date())
    print("Priority:3\n")
    print("Processing query:" + query_to_be_processed.encode("utf-8") + " in "+ lang + " of " + date)
    raw_data = tw_util.get_tweets_from_search_cleaned(query_to_be_processed,n_items_search=1000,n_tweets_per_user=100,lang=lang)
    mlab.update_status_collected(query_to_be_processed,lang,date,True) 
    if len(raw_data["users"])<50:
        print("Too few users for your query")
        mlab.update_status_collected(query_to_be_processed,lang,date,"Too few users")
        mlab.update_status_clustered(query_to_be_processed,lang,date,"Too few users")
        mlab.update_priority(query_to_be_processed,lang,date,3)
        mlab.update_priority(query_to_be_processed,lang,FormerDate,False)
    else:
        # mlab.upload_twitter_raw(raw_data)
        cluster_data = clust.cluster_tweets(raw_data)
        cluster_data["date"]=date
        cluster_data["language"]=lang
        mlab.upload_twitter_community(cluster_data)
        mlab.update_status_clustered(query_to_be_processed,lang,date,True)
        mlab.update_priority(query_to_be_processed,lang,date,2)
        mlab.update_priority(query_to_be_processed,lang,FormerDate,False)
    print("All done in %f minutes!" % ((time() - t0) / 60))    
else:
    print("No job in the queue")
