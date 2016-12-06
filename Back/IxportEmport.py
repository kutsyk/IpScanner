from pymongo.mongo_client import MongoClient
# from cloud import *

# cloudClient = Cloud()
mongoClient = MongoClient()
ipDB = mongoClient.ipstats
ipDevCollection = ipDB.ips_dev

# docs = list(cloudClient.CLIENT.QueryDocuments(cloudClient.banners['_self'], "Select * from c"))
# for i,doc in enumerate(docs):
#     ipDevCollection.insert(doc)
#     print i

for doc in ipDevCollection.find():
    print doc