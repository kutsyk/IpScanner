#!/usr/bin/python
import nmap
from netaddr import *
from cloud import *

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 1 --min-parallelism 16 -sV -Pn --script=http-title --script=http-headers -T5"

def scan(host):
    nm.scan(hosts=host, arguments=args)
    for h in nm.all_hosts():
        print "------------------------"
        print nm[h]
    # if host.Address in nm.all_hosts():
        # CLIENT.CreateDocument(banners_dev['_self'], {
            # 'id': host.PartitionKey + '_id_' + host.Address,
            # 'info': nm[host.Address]
        # })


ipNet = IPNetwork('31.131.16.0/20')
for ip in ipNet:
    print ip
