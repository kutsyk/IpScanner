from MyCloud import *
import json

mongoClient = MongoConnector('local')
ipDB = mongoClient.ipStats
ipDevCollection = ipDB.ips_banners
TCP = "tcp"

def ProcessBanner(banner):
    info = banner["info"]
    banObj = json.loads(info)

    banner["status"] = banObj["status"]
    banner["ip"] = banObj["addresses"]["ipv4"]
    banner["hostnames"] = banObj["hostnames"]

    if TCP in banObj.keys():
        banner["ports"] = []
        for item in banObj["tcp"]:
            banner["ports"].append(item)

        for port in banner["ports"]:
            banner[str(port)] = banObj["tcp"][str(port)]
    # tcp is null
    return banner


i = 0
for banner in ipDevCollection.find():
    ipDevCollection.save(ProcessBanner(banner))
    if i % 1000 == 0:
        print i
    i += 1