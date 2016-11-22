#!/usr/bin/python
from netaddr import *
import nmap
import pydocumentdb.document_client as document_client

# DOCUMENTDB_HOST = 'https://ipstats.documents.azure.com:443/'
# DOCUMENTDB_KEY = 'FuRTjt01UVmWS1KRPxkbLxOw7imKhNyHIWluSxZ8rjwZrJSZwJKJUNBYhAzDsiOHk2yKdzv9JhQOuEHWtDhZ4w=='

# DOCUMENTDB_COLLECTION = 'host-banners'
# DOCUMENTDB_DATABASE = 'dbs/host-banners'

# CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
# DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
# DOCUMENTS_COLL = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
# banners = DOCUMENTS_COLL[0]
# banners_dev = DOCUMENTS_COLL[1]

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


# with open('CIDR.txt', 'r') as cidr_file:
    # lines = cidr_file.readlines()
    # size = 0
    # for host in lines:
    #     if host.startswith("#"):
    #         continue
ipNet = IPNetwork('31.131.16.0/20')
for ip in ipNet:
    print ip

    # print size
    # print cidr_file.read()
