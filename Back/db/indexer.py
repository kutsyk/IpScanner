from elasticsearch import Elasticsearch
import json
import netaddr
import requests
from MyCloud import *
es = Elasticsearch()

mongoClient = MongoConnector('local')
ipDB = mongoClient.ipStats
ipDevCollection = ipDB.ips_banners

def addToIndex(banner, id):
    del banner["_id"]
    del banner["info"]
    try:
        res = es.index(index="ipstats", doc_type='banner', id=id, body=banner)
    except Exception as e:
        print e

i = 0
for banner in ipDevCollection.find():
    addToIndex(banner, i)
    if i % 100 == 0:
        print i
    i += 1
