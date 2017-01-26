#!/usr/bin/python
from pymongo.mongo_client import MongoClient

MONGODB_URI = "mongodb://user:pass@52.178.187.80:27017/ipstats"
MONGODB_LOCAL_URI = "mongodb://localhost:27017/ipstats"

class MongoConnector:
    def __init__(self, host=None):
        if host is None:
            self.mongoClient = MongoClient(MONGODB_URI)
        else:
            self.mongoClient = MongoClient(MONGODB_LOCAL_URI)
        self.ipDBProd = self.mongoClient.get_default_database()
        self.ipDBDev = self.mongoClient.ipstats
        self.ipStats = self.mongoClient.ipstats

        self.ipDevBanners = self.ipDBDev.ips_dev

        self.ipsBanners = self.ipDBProd.ips_banners
        self.ipsHosts = self.ipDBProd.ips_hosts
        self.processedIps = self.ipDBProd.processed_ips

#if len(args) == 1:
	#docs = list(CLIENT.QueryDocuments(banners_dev['_self'], "Select * from c"))
#elif args[1]:
	#docs = list(CLIENT.QueryDocuments(banners['_self'], "Select * from c"))
#print len(docs)
