#!/usr/bin/python
from pymongo.mongo_client import MongoClient

MONGODB_URI = "mongodb://user:pass@ds133348.mlab.com:33348/ipstats"

class MongoConnector:
    mongoClient = MongoClient(MONGODB_URI)
    ipDBProd = mongoClient.get_default_database()

    ipDBDev = mongoClient.ipstats
    ipDevBanners = ipDBDev.ips_dev

    ipsBanners = ipDBProd.ips_banners
    ipsHosts = ipDBProd.ips_hosts

#args = sys.argv

#if len(args) == 1:
	#docs = list(CLIENT.QueryDocuments(banners_dev['_self'], "Select * from c"))
#elif args[1]:
	#docs = list(CLIENT.QueryDocuments(banners['_self'], "Select * from c"))
#print len(docs)