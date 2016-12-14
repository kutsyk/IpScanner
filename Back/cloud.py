#!/usr/bin/python
import sys
import pydocumentdb.document_client as document_client
import ConfigParser
import pymongo
from pymongo.mongo_client import MongoClient

# class Cloud:
#     configParser = ConfigParser.RawConfigParser()
#     configFilePath = r'config.txt'
#     configParser.read(configFilePath)
#
#     DOCUMENTDB_HOST = configParser.get('cloud-config', 'DOCUMENTDB_HOST')
#     DOCUMENTDB_KEY = configParser.get('cloud-config', 'DOCUMENTDB_KEY')
#
#     DOCUMENTDB_COLLECTION = configParser.get('cloud-config', 'DOCUMENTDB_COLLECTION')
#     DOCUMENTDB_DATABASE = configParser.get('cloud-config', 'DOCUMENTDB_DATABASE')
#
#     CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
#     DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
#     DOCUMENTS_COLL = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
#     banners = DOCUMENTS_COLL[0]
#     banners_dev = DOCUMENTS_COLL[1]

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
