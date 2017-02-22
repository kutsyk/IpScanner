import json
import netaddr
import requests
from MyCloud import *

mongoClient = MongoConnector('local')
ipDB = mongoClient.ipStats
ipDevCollection = ipDB.ips_banners
TCP = "tcp"
ripeHeader = {'Accept': 'application/json'}


# def ReformatAddress(address):
# remove numbers
# address = ''.join(i for i in address if not i.isdigit())
# address =
# address = address.replace("str.", "St")
# return ''.join(i for i in address if not i.isdigit())

def getAddress(ip):
    response = requests.get('http://freegeoip.net/json/' + ip)
    return json.loads(response.content)

def contains(banner, key):
    return key in banner.keys() and banner[key]


def isNone():
    return banner["status"] is None


def ProcessBanner(banner):
    info = banner["info"]
    banObj = json.loads(info)
    ip = banObj["addresses"]["ipv4"]

    if not contains(banner, "status"):
        banner["status"] = banObj["status"]
    if not contains(banner, "ip"):
        banner["ip"] = ip
    if not contains(banner, "address"):
        address = getAddress(ip)
        banner["address"] = address
    if not contains(banner, "dec_ip"):
        banner["dec_ip"] = int(netaddr.IPAddress(banObj["addresses"]["ipv4"]))
    if not contains(banner, "hostnames"):
        banner["hostnames"] = banObj["hostnames"]

    if TCP in banObj.keys():
        if not contains(banner, "ports"):
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
    if i % 100 == 0:
        print i
    i += 1
