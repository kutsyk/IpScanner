#!/usr/bin/python
from threading import Thread
import threading
import nmap
from Queue import Queue
import time
from azure.storage.table import TableService, Entity
from time import gmtime, strftime


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

def main():
    host = '85.90.221.244'
    # Set up some threads to fetch the enclosures

    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)
    ip_queue.put(host)

    for i in xrange(available_threads):
        worker = Thread(target=scnner_function, args=(i, ip_queue))
        worker.setDaemon(True)
        worker.start()

    ip_queue.join()

if __name__ == '__main__':
    main()
