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
# Read data from Azure table

CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
ERRORS_DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='errors'"))

document_coll = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
errors_coll = list(CLIENT.ReadCollections(ERRORS_DATABASE))

banners = document_coll[0]
errors = errors_coll[0]

table_service = TableService(account_name='ipstats',
                             account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

nm = nmap.PortScanner()


def scnner_function(i, owner, q):
    print "Thread %d: started" % i
    while True:
        host = q.get()
        try:
            nm.scan(host, arguments="-O")
            CLIENT.CreateDocument(banners['_self'], {
                'id': owner + '_id_' + host,
                'info': nm[host]
            })
        except BaseException as e:
            CLIENT.CreateDocument(errors['_self'], {
                'id': owner + '_id_' + host,
                'message': e.message
            })
        q.task_done()

def main():
    owners = table_service.query_entities('owners')
    for owner in owners:
        ipAddresses = table_service.query_entities('ipAddress', filter="PartitionKey eq '" + owner.Name + "'")
        for ip in ipAddresses:
            ip_queue.put(ip.Address)

        for i in xrange(available_threads):
            worker = Thread(target=scnner_function, args=(i, owner.Name, ip_queue))
            worker.setDaemon(True)
            worker.start()

        ip_queue.join()
        ip_queue.queue.clear()


if __name__ == '__main__':
    main()
