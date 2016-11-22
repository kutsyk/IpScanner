#!/usr/bin/python
from threading import Thread
import threading
import nmap
from azure.storage.table import TableService
import pydocumentdb.document_client as document_client
from scapy.layers.inet import *
from Queue import Queue
from netaddr import *

DOCUMENTDB_HOST = 'https://ipstats.documents.azure.com:443/'
DOCUMENTDB_KEY = 'FuRTjt01UVmWS1KRPxkbLxOw7imKhNyHIWluSxZ8rjwZrJSZwJKJUNBYhAzDsiOHk2yKdzv9JhQOuEHWtDhZ4w=='

DOCUMENTDB_COLLECTION = 'banners'
DOCUMENTDB_COLLECTION_DEV = 'banners-dev'
DOCUMENTDB_DATABASE = 'dbs/host-banners'

available_threads = 8

CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
DOCUMENTS_COLL = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
banners = DOCUMENTS_COLL[0]
banners_dev = DOCUMENTS_COLL[1]

table_service = TableService(account_name='ipstats',
                             account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

nextPartKey = None
nextRowKey = None
ipNetworksQueue = Queue()
TIMEOUT = 5

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 1 -sV -Pn --script=http-title --script=http-headers"
def scan(host, nm):
    # TODO: geolocation script --script ip-geolocation-geoplugin
    pack = IP(dst=host)/ICMP()
    reply = sr1(pack, timeout=TIMEOUT, verbose=False)
    if reply is not None:
        nm.scan(host, arguments=args)
        if host in nm.all_hosts():
            CLIENT.CreateDocument(banners['_self'], {
                'id': 'id_' + host,
                'info': nm[host]
            })

def scanner_function(i, q):
    print "Thread ", i
    while True:
        network = q.get()

        ipNet = IPNetwork(network)
        for ip in ipNet:
            scan(str(ip), nm)

        q.task_done()


def main():
    workers = []
    with open('CIDR.txt', 'r') as cidr_file:
        line = cidr_file.readlines()
        for l in line:
            if l.startswith("#"):
                continue
            ipNetworksQueue.put(l)

    for i in xrange(available_threads):
        worker = Thread(target=scanner_function, args=(i, ipNetworksQueue))
        worker.setDaemon(True)
        workers.append(worker)

    for worker in workers:
        worker.start()

    ipNetworksQueue.join()

if __name__ == '__main__':
    main()
