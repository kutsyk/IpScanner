#!/usr/bin/python
import sys
import json
import bson
from netaddr import IPNetwork
import netaddr
from MyCloud import *

ThreadConn = MongoConnector()

def main():
    print "IpSaver started"    
    with open('CIDR.txt', 'r') as cidr_file:
        line = cidr_file.readlines()
        for l in line:
            if l.startswith("#"):
                continue
            ipNet = IPNetwork(l)
            for ip in ipNet:
                ThreadConn.processedIps.insert(
                { "_id" : int(netaddr.IPAddress(ip)) }
                )
    print "IpSaver finished"


if __name__ == '__main__':
    main()
