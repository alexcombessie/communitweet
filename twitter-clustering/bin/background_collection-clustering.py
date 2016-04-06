# coding=utf-8
# Importing necessary libraries
import os
import sys
from time import time

t0 = time()

# Importing custom modules
from twitterapp.twscrap import TwitterApiUtil

tw_util = TwitterApiUtil()

import twitterapp.mongolab as mlab
import twitterapp.docluster as clust

try:
    current_query_status = mlab.download_query()
    index_to_be_processed = [t["collected"] for t in current_query_status].index(False)
    query_to_be_processed = [t["query"] for t in current_query_status][index_to_be_processed]
    print("Processing " + query_to_be_processed.encode("utf-8"))

    raw_data = tw_util.get_tweets_from_search_cleaned(query_to_be_processed,n_items_search=1200,n_tweets_per_user=200)
    mlab.update_status_collected(query_to_be_processed)
    if len(raw_data["users"])<50:
        print("Too few users for your query")
        mlab.update_status_collected(query_to_be_processed,"Too few users")
        mlab.update_status_clustered(query_to_be_processed,"Too few users")
    else:
        # mlab.upload_twitter_raw(raw_data)
        cluster_data = clust.cluster_tweets(raw_data)
        mlab.upload_twitter_community(cluster_data)
        mlab.update_status_clustered(query_to_be_processed)

        print("All done in %f minutes!" % ((time() - t0) / 60))

except ValueError:
    print("No job in the queue")
