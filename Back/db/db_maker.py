from MyCloud import *
import json
import netaddr

mongoClient = MongoConnector('local')
ipDB = mongoClient.ipStats
ipDevCollection = ipDB.ips_banners
TCP = "tcp"

def isNone(obj):
    return banner["status"] is None

def ProcessBanner(banner):
    info = banner["info"]
    banObj = json.loads(info)

    if not ("status" in banner.keys()):
        banner["status"] = banObj["status"]
    if not ("ip" in banner.keys()):
        banner["ip"] = banObj["addresses"]["ipv4"]
    if not ("dec_ip" in banner.keys()):
        banner["dec_ip"] = int(netaddr.IPAddress(banObj["addresses"]["ipv4"]))
    if not ("hostnames" in banner.keys()):
        banner["hostnames"] = banObj["hostnames"]

    if TCP in banObj.keys():
        if not ("ports" in banner.keys()):
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