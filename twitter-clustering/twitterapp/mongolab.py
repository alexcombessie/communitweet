# coding=utf-8
# Load data to Mongolab and download query results from Mongolab

import json
import os
import time

from pymongo import MongoClient

# Open mongolab connection
client = MongoClient(os.environ.get('MONGOLAB_URI'))
db = client.ensae_twitter


# Upload json file to the collection in MongoLab (replace collection by collection name before running)

def upload_twitter_query(dict_object):
    time.sleep(1)
    print("Uploading Twitter data to mLab...")
    db.twitter_query.insert_one(json.loads(json.dumps(dict_object)))


def upload_twitter_raw(dict_object):
    time.sleep(1)
    print("Uploading Twitter data to mLab...")
    db.twitter_raw.insert_one(json.loads(json.dumps(dict_object)))


def upload_twitter_community(dict_object):
    time.sleep(1)
    print("Uploading community structure to mLab...")
    db.twitter_community.insert_one(json.loads(json.dumps(dict_object)))


# Download query result from Mongolab (replace collection by collection name before running)
def download_query():
    results = db.twitter_query.find()
    return (list(results))


def download_raw(query):
    print("Downloading Twitter data from mLab...")
    results = db.twitter_raw.find({"query": str(query)})
    return (list(results)[-1])


def download_community(query):
    print("Downloading community structure from mLab...")
    results = db.twitter_community.find({"query": str(query)})
    return (list(results)[-1])


def update_status_collected(query, modif=True):
    db.twitter_query.update_one(
        {"query": query},
        {
            "$set": {
                "collected": modif
            }
        }
    )


def update_status_clustered(query, modif=True):
    db.twitter_query.update_one(
        {"query": query},
        {
            "$set": {
                "community": modif
            }
        }
    )


def clear_all_db():
    db.twitter_query.delete_many({})
    db.twitter_raw.delete_many({})
    db.twitter_community.delete_many({})

def delete_query(query):
    db.twitter_query.delete_many({"query": query})
