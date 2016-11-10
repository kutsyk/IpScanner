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

available_threads = 8
ip_queue = Queue()
# Read data from Azure table

# table_service = TableService(account_name='ipstats', account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

# owners = table_service.query_entities('owners')
# owner = owners[5]
# print(owner.ExpectedAmount)
# for owner in owners:

# ipAddresses = table_service.query_entities('ipAddress', filter="PartitionKey eq '"+owner.Name+"'")
# for ip in ipAddresses:
#     print(ip.Address)

nm = nmap.PortScanner()


def scnner_function(i, q):
    print "Thread %d: started" % i
    while True:
        host = q.get()
        nm.scan(host, arguments="-O")
        print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print "\n"
        print nm[host]['tcp']
        print "\n"
        q.task_done()


DOCUMENTDB_DOCUMENT = 'test'


def main():
    host = '85.90.221.244'
    # Set up some threads to fetch the enclosures

    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)
    # ip_queue.put(host)

    # for i in xrange(available_threads):
    #     worker = Thread(target=scnner_function, args=(i, ip_queue))
    #     worker.setDaemon(True)
    #     worker.start()

    # ip_queue.join()

    client = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
    db = list(client.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
    # print db
    # print len(db)
    d = db[0]
    collections = list(client.ReadCollections(DOCUMENTDB_DATABASE))
    c = collections[0]
    # Create document
    print c
    document = client.CreateDocument(c['_self'],
                                     {'id': DOCUMENTDB_DOCUMENT,
                                      'test0': 0,
                                      'test1': 0,
                                      'test2': 0,
                                      'name': DOCUMENTDB_DOCUMENT
                                      })


if __name__ == '__main__':
    main()
