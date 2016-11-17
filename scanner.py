#!/usr/bin/python
from threading import Thread
import threading
import nmap
from azure.storage.table import TableService
import pydocumentdb.document_client as document_client
from scapy.layers.inet import *

DOCUMENTDB_HOST = 'https://ipstats.documents.azure.com:443/'
DOCUMENTDB_KEY = 'FuRTjt01UVmWS1KRPxkbLxOw7imKhNyHIWluSxZ8rjwZrJSZwJKJUNBYhAzDsiOHk2yKdzv9JhQOuEHWtDhZ4w=='

DOCUMENTDB_COLLECTION = 'host-banners'
DOCUMENTDB_DATABASE = 'dbs/host-banners'

available_threads = 8

CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
DOCUMENTS_COLL = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
banners = DOCUMENTS_COLL[0]

table_service = TableService(account_name='ipstats',
                             account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

nextPartKey = None
nextRowKey = None
nm = nmap.PortScanner()

def scan(host, nm):
    # TODO: geolocation script --script ip-geolocation-geoplugin

    pack = IP(dst=host) / ICMP()
    reply = sr1(pack, timeout=10)
    if reply is None:
        print "Down"
    else:
        print "Up"
    # nm.scan(host.Address, arguments="-Pn -O -A")
    # if host.Address in nm.all_hosts():
    #     CLIENT.CreateDocument(banners['_self'], {
    #         'id': host.PartitionKey + '_id_' + host.Address,
    #         'info': nm[host.Address]
    #     })

def scnner_function(i, lock):
    print "Thread ", i
    global nextPartKey
    global nextRowKey

    while True:
        with lock:
            oneObjectList = table_service.query_entities('ipAddress', filter='', top=1, next_partition_key=nextPartKey,
                                                         next_row_key=nextRowKey)
            currentIp = oneObjectList.pop()
            nextPartKey = oneObjectList.x_ms_continuation['NextPartitionKey']
            nextRowKey = oneObjectList.x_ms_continuation['NextRowKey']
            if not nextPartKey and not nextRowKey:
                break
        scan(currentIp, nm)

def main():
    workers = []
    lock = threading.Lock()
    for i in xrange(available_threads):
        worker = Thread(target=scnner_function, args=(i, lock))
        worker.setDaemon(True)
        workers.append(worker)

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()


if __name__ == '__main__':
    main()
