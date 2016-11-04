#!/usr/bin/python
from threading import Thread
import threading
import nmap
from Queue import Queue
import time
from azure.storage.table import TableService, Entity
from time import gmtime, strftime


available_threads = 2
ip_queue = Queue()

# table_service = TableService(account_name='ipstats', account_key='yjtopnZUk0TvdrNixtWUGcyt0FJuUwolOFFLiwpUtFWHBSt9L4i/AsBWo4Hnpsd+Thf5xNCKczntE4MOM3XqRA==')

# owners = table_service.query_entities('owners')
# owner = owners[5]
# print(owner.ExpectedAmount)
# for owner in owners:

# ipAddresses = table_service.query_entities('ipAddress', filter="PartitionKey eq '"+owner.Name+"'")
# for ip in ipAddresses:
#     print(ip.Address)

# def scnner_function(i, q):
#     print "Thread %d: started" % i
#     while True:
#         host = q.get()
#         nm.scan(host, arguments="-O")
#         print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#         print "\n"
#         print nm.scaninfo()
#         print "\n"
#         q.task_done()

def main():

    # '31.131.19.12'
    scanner1 = nmap.PortScanner()

    start_time = time.time()
    host = '85.90.221.245'
    print scanner1.scan(host, arguments='-A -O')
    print("--- %s seconds ---" % (time.time() - start_time))

    print scanner1.command_line()
    print scanner1.scaninfo()
    print scanner1.all_hosts()
    print scanner1[host].all_protocols()
    print scanner1[host]['tcp']
    print scanner1[host]['tcp'][80]
    # print scanner1['31.131.19.12'].state()
    # scanner2 = nmap.PortScannerAsync().scan('31.131.19.12')
    # Set up some threads to fetch the enclosures

    # ip_queue.put('31.131.19.12')
    # ip_queue.put('31.131.19.12')
    # ip_queue.put('31.131.19.12')

    # for i in xrange(available_threads):
    #     worker = Thread(target=scnner_function, args=(i, ip_queue))
    #     worker.setDaemon(True)
    #     worker.start()

    # ip_queue.join()
    # make_requests()
    # scanIpAddress(nma, 'empty')

if __name__ == '__main__':
    main()