import json
from threading import *
import requests
import httplib
from MyCloud import *

mongoClient = MongoConnector('local')
ipDB = mongoClient.ipStats
ipDevCollection = ipDB.ips_banners


# def ReformatAddress(address):
# remove numbers
# address = ''.join(i for i in address if not i.isdigit())
# address =
# address = address.replace("str.", "St")
# return ''.join(i for i in address if not i.isdigit())

def getRipeInfo(banner, ip):
    try:
        headers = {'Accept': 'application/json'}
        connLine = 'http://rest.db.ripe.net/search?source=ripe&query-string=' + ip
        res = requests.get(connLine, headers=headers)
        banner["ripe"] = res.json()["objects"]["object"]
    except Exception as e:
        print e

def getAddress(ip):
    response = requests.get('http://freegeoip.net/json/' + ip)
    return json.loads(response.content)


def processAddress(banner, ip):
    if not contains(banner, "address"):
        address = getAddress(ip)
        banner["address"] = address


def processHeadersThread(banner, ip):
    if 'ports' in banner.keys():
        for port in banner["ports"]:
            processHeaders(banner, ip, port)


def processHeaders(banner, ip, port):
    conn = httplib.HTTPConnection(ip, port, timeout=1000)
    try:
        conn.request("HEAD", "/")
        res = conn.getresponse()
        if res.status == 200:
            headers = res.getheaders()
            res = {}
            for (key, val) in headers:
                res[key] = val
            banner[port + ""]["headers"] = res
    except Exception:
        return None


def contains(banner, key):
    return key in banner.keys() and banner[key]


def ProcessBanner(banner):
    ip = banner["ip"]
    t1 = Thread(target=processAddress, args=(banner, ip))
    t2 = Thread(target=processHeadersThread, args=(banner, ip))
    t3 = Thread(target=getRipeInfo, args=(banner, ip))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    # tcp is null
    return banner


i = 0
for banner in ipDevCollection.find():
    ipDevCollection.save(ProcessBanner(banner))
    if i % 10 == 0:
        print i
    i += 1
