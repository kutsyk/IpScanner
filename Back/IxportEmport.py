from pymongo.mongo_client import MongoClient

mongoClient = MongoClient()
ipDB = mongoClient.ipstats
ipDevCollection = ipDB.ips_dev

for doc in ipDevCollection.find():
    print doc