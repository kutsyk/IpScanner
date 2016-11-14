#!/usr/bin/python
from threading import Thread
import nmap
from Queue import Queue
from azure.storage.table import TableService, Entity
import pydocumentdb.document_client as document_client
from time import gmtime, strftime

DOCUMENTDB_HOST = 'https://ipstats.documents.azure.com:443/'
DOCUMENTDB_KEY = 'FuRTjt01UVmWS1KRPxkbLxOw7imKhNyHIWluSxZ8rjwZrJSZwJKJUNBYhAzDsiOHk2yKdzv9JhQOuEHWtDhZ4w=='

DOCUMENTDB_COLLECTION = 'host-banners'
DOCUMENTDB_DATABASE = 'dbs/host-banners'
ERRORS_DATABASE = 'dbs/errors'

available_threads = 8
ip_queue = Queue()
OWNER_NAME = ''
# Read data from Azure table

CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
document_coll = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))

banners = document_coll[0]

table_service = TableService(account_name='ipstats',
                             account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

nm = nmap.PortScanner()

def scan(i, q):
    host = q.get()
    # TODO: geolocation script --script ip-geolocation-geoplugin
    nm.scan(host, arguments="-O -A")
    if host in nm.all_hosts():
        CLIENT.CreateDocument(banners['_self'], {
            'id': OWNER_NAME + '_id_' + host,
            'info': nm[host]
        })
    q.task_done()

def scnner_function(i, q):
    print "Thread %d: started" % i
    while True:
        scan(i, q)    

def main():
    owners = table_service.query_entities('owners')
	
    workers = []
    for i in xrange(available_threads):
        worker = Thread(target=scnner_function, args=(i, ip_queue))
        worker.setDaemon(True)
        workers.append(worker)

    for owner in owners:
            ipAddresses = table_service.query_entities('ipAddress', filter="PartitionKey eq '" + owner.Name + "'")

            for ip in ipAddresses:
                ip_queue.put(ip.Address)
            global OWNER_NAME
            OWNER_NAME = owner.Name
            
            for worker in workers:
                worker.start()

            ip_queue.join()
            ip_queue.queue.clear()

if __name__ == '__main__':
    main()
