# coding=utf-8
# Load data to Mongolab and download query results from Mongolab

from random import sample,choice
import urllib
import json
import os
import time
import datetime 
from pymongo import MongoClient

# Open mongolab connection
client = MongoClient(os.environ.get('MONGOLAB_URI'))
db = client.ensae_twitter


# Upload json file to the collection in MongoLab (replace collection by collection name before running)

def upload_twitter_query(dict_object):
    time.sleep(1)
    print("Uploading Twitter data to mLab...")
    db.twitter_query1.insert_one(json.loads(json.dumps(dict_object)))


def upload_twitter_raw(dict_object):
    time.sleep(1)
    print("Uploading Twitter data to mLab...")
    db.twitter_raw.insert_one(json.loads(json.dumps(dict_object)))


def upload_twitter_community(dict_object):
    time.sleep(1)
    print("Uploading community structure to mLab...")
    db.twitter_community1.insert_one(json.loads(json.dumps(dict_object)))

def checkLastFiveResultsPriority3():
    results = list(db.twitter_query1.find({"Priority":3}))
    now = datetime.datetime.now().date()
    results = [i for i in results if (now-datetime.datetime.strptime(str(i["date of processing"]),'%Y-%m-%d').date()).days >= 7]
    while len(results)>0:
        query=choice(results)
        PastQueries=[j for j in list(db.twitter_query1.find({"query":query["query"],"language":query["language"],"Priority":{"$in":[3,False]}}))]
        Dates=[]
        for k in PastQueries:
            Dates.append(datetime.datetime.strptime(k["date"],'%Y-%m-%d').date())
        Dates=sorted(Dates)
        query=list(db.twitter_query1.find({"query":query["query"],"language":query["language"],"date":str(max(Dates)),"Priority":{"$in":[3,False]}}))
        if len(Dates)>=5:
            for l in range(1,6):
                a=list(db.twitter_query1.find({"query":query[0]["query"],"language":query[0]["language"],"date":str(Dates[-l]),"Priority":{"$in":[3,False]}}))
                if a[0]["collected"] != "Too few users":
                    query[0]["check"]=True
                    uploadToMongolab(query[0]["query"],query[0]["language"],3)
                    update_processing_date(query[0]["query"],query[0]["language"],str(now))
                    return query[0]
            results.remove(query[0])
            print("This query has been tried too much")
            uploadToMongolab(query[0]["query"],query[0]["language"],False)
            update_processing_date(query[0]["query"],query[0]["language"],str(now))
            update_status_collected(query[0]["query"],query[0]["language"],str(now),"Too few users")
            update_status_clustered(query[0]["query"],query[0]["language"],str(now),"Too few users")      
            update_priority(query[0]["query"],query[0]["language"],query[0]["date"],False)
        else:
            query[0]["check"]=True
            uploadToMongolab(query[0]["query"],query[0]["language"],3)
            update_processing_date(query[0]["query"],query[0]["language"],str(now))
            return query[0] 
    return {"check":False}
    

# Download query result from Mongolab (replace collection by collection name before running)
def download_query():
    now = datetime.datetime.now().date()
    results = list(db.twitter_query1.find({"Priority":2}))
    results = [i for i in results if (now-datetime.datetime.strptime(str(i["date of processing"]),'%Y-%m-%d').date()).days >= 7]
    Prio3=checkLastFiveResultsPriority3()
    if db.twitter_query1.find({'Priority': 1}).count() > 0:
        results = list(db.twitter_query1.find({"Priority":1}))
        query=choice(results)
        return (query)
    elif len(results) > 0:
        query=choice(results)
        return (query)
    elif Prio3["check"]:
        query = Prio3
        return (query)
    else:
        return {"Priority":False}        

def download_raw(query):
    print("Downloading Twitter data from mLab...")
    results = db.twitter_raw.find({"query": str(query)})
    return (list(results)[-1])


def download_community(query):
    print("Downloading community structure from mLab...")
    results = db.twitter_community1.find({"query": str(query)})
    return (list(results)[-1])


def update_status_collected(query, lang, date, modif=True):
    db.twitter_query1.update_one(
        {"query": query, "language":lang,"date":date},
        {
            "$set": {
                "collected": modif
            }
        }
    )


def update_status_clustered(query,lang,date, modif=True):
    db.twitter_query1.update_one(
        {"query": query, "language":lang,"date":date},
        {
            "$set": {
                "community": modif
            }
        }
    )

def update_processing_date(query,lang,date):
    db.twitter_query1.update_one(
        {"query": query, "language":lang,"date":date},
        {
            "$set": {
                "date of processing": str(datetime.datetime.now().date())
            }
        }
    )

def update_priority(query,lang,date,priority):
    db.twitter_query1.update_one(
        {"query": query, "language":lang,"date":date},
        {
            "$set": {
                "Priority": priority
            }
        }
    )
    
def clear_all_db():
    db.twitter_query1.delete_many({})
    db.twitter_raw.delete_many({})
    db.twitter_community1.delete_many({})

def delete_query(query):
    db.twitter_query1.delete_many({"query": query})

def FindTheMostRecentResult(text,lang):
    text = text.strip().lower()
    lang = lang.strip().lower()
    c=db.twitter_community1.find({'query': text, 'language':lang})
    result=list(c)
    Dates=[]
    for i in range(0,len(result)):
        Dates.append(result[i]['date'])
    return str(max(Dates))


def chooseQueryRandomly(lang):
    c=list(db.twitter_community1.find({"language": lang}))
    randomqueries = []
    Dates=[]
    Queries=[]
    query=choice(c)
    randomqueries.append(query["query"])
    Dates.append(FindTheMostRecentResult(query["query"],lang))
    for i in range(1,5):
        query=choice(c)
        while query["query"] in randomqueries:
            query=choice(c)
        randomqueries.append(query["query"])
        Dates.append(FindTheMostRecentResult(query["query"],lang))
    Queries.append(randomqueries)
    Queries.append(Dates)
    return (Queries)

def changeLanguageCharacterString(lang):
    if lang=='en':
        newstring='English'
    elif lang=='fr':
        newstring='French'
    elif lang=='de':
        newstring='German'
    elif lang=='nl':
        newstring='Dutch'
    elif lang=='es':
        newstring='Spanish'
    elif lang=='it':
        newstring='Italian'
    return(newstring)

def Encoding(query):
    query = query.strip().lower().encode("utf-8", errors="ignore")
    text=query    
    #text = urllib.urlencode({"query":query}).split("=")[1]
    return text
   
def uploadToMongolab(text,lang,priority):
    line = {'query' : text, 'collected': False, 'community': False, 'date': str(datetime.datetime.now().date()), 'language': lang, "Priority":priority}
    if line != "\n":
      db.twitter_query1.insert_one(line)

def AlreadyInCollectionQuery(text,language):
    text = text.strip().lower()
    language = language.strip().lower()
    results=db.twitter_query1.find({'query': text, 'language':language})
    if results.count() == 0:
        return "No"
    Dates=[]
    for k in results:
        Dates.append(datetime.datetime.strptime(k["date"],'%Y-%m-%d').date())
    query=db.twitter_query1.find({"query":text,"language":language,"date":str(max(Dates))})
    if query[0]["Priority"] == 3:
        return "Too few users"
    elif query[0]["Priority"] == 1 or query[0]["Priority"] == 2:
        return "Yes"
    else:
        return "No"

def AlreadyInCollectionCommunity(text,language):
    text = text.strip().lower()
    language = language.strip().lower()
    if db.twitter_community1.find({'query': text,"language": language}).count() > 0:
        return True
    else:
        return False

def downloadOtherResultsForTheQuery(query):
    FormerQueries=list(db.twitter_query1.find({"query":query}))
    results={"Dutch":[],"English":[],"French":[],"German":[],"Italian":[],"Spanish":[]}
    for j in FormerQueries:
        if j["language"] == "nl":
            results["Dutch"].append(j)
        elif j["language"] == "en":
            results["English"].append(j)
        elif j["language"] == "fr":
            results["French"].append(j)
        elif j["language"] == "de":
            results["German"].append(j)
        elif j["language"] == "it":
            results["Italian"].append(j)
        elif j["language"] == "es":
            results["Spanish"].append(j)
    return results
        
            

def FindTheMostRecentResult(text,lang):
    text = text.strip().lower()
    lang = lang.strip().lower()
    c=db.twitter_community1.find({'query': text, 'language':lang})
    result=list(c)
    Dates=[]
    for i in range(0,len(result)):
        Dates.append(result[i]['date'])
    return str(max(Dates))

def getCommunityInfo(text,lang,date):
    results_cursor = db.twitter_community1.find({'query': text,"language":lang,"date":date})
    for document in results_cursor:
        return document

def communityInfo(text,lang,date,i):
    raw_result = getCommunityInfo(text,lang,date)
    community_i = raw_result['communities'][i]
    result = {}
    result['size'] = len(community_i['screen_names'])
    result['words'] = community_i['words']
    return result

def communitySize(text,lang,date,i):
    raw_result = getCommunityInfo(text,lang,date)
    community_i = raw_result['communities'][i]
    result = len(community_i['screen_names'])
    return result

def communitySizePercent(text,lang,date, i):
    comSize = communitySize(text,lang,date,i)
    totalSize = communitySize(text,lang,date,0) + communitySize(text,lang,date, 1) + communitySize(text,lang,date, 2) + communitySize(text,lang,date, 3)
    return format(comSize/float(totalSize) * 100, '.2f')

def communityWords(text,lang,date,i):
    raw_result = getCommunityInfo(text,lang,date)
    community_i = raw_result['communities'][i]
    max_weight = community_i['words'][0]['weight']
    factor = 3
    results = []
    for i in range(len(community_i['words'])):
        if community_i['words'][i]['weight'] > max_weight/factor:
            results.append(community_i['words'][i])
    return results

client.close()
