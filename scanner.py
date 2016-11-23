#!/usr/bin/python
import nmap
from threading import Thread
from Queue import Queue
import pydocumentdb.document_client as document_clien
from scapy.layers.inet import *
from netaddr import *
from cloud import *

AVAILABLE_THREADS = 16
TIMEOUT = 5
ipNetworksQueue = Queue()

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 0 -sV -Pn --script=http-title --script=http-headers"

def scan(host, nm):
    # TODO: geolocation script --script ip-geolocation-geoplugin
    pack = IP(dst=host) / ICMP()
    reply = sr1(pack, timeout=TIMEOUT, verbose=False)
    if reply is not None:
        nm.scan(host, arguments=args)
        if host in nm.all_hosts():
            if nm[host].state() == 'up':
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

    for i in xrange(AVAILABLE_THREADS):
        worker = Thread(target=scanner_function, args=(i, ipNetworksQueue))
        worker.setDaemon(True)
        workers.append(worker)

    for worker in workers:
        worker.start()

    ipNetworksQueue.join()


if __name__ == '__main__':
    main()
