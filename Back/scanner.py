#!/usr/bin/python
import sys
import nmap
import json
from threading import Thread
from Queue import Queue
import gc
from scapy.layers.inet import *
from netaddr import *
from cloud import *

AVAILABLE_THREADS = 32
TIMEOUT = 5
ipNetworksQueue = Queue()

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 0 -sV -Pn --script=http-title --script=http-headers"

def scan(conn, host, nm, icmp):
    # TODO: geolocation script --script ip-geolocation-geoplugin
    pack = IP(dst=host) / icmp
    reply = sr1(pack, timeout=TIMEOUT, verbose=False)
    if reply is not None:
        try:
            nm.scan(host, arguments=args)
            if host in nm.all_hosts():
                if nm[host].state() == 'up':
                    conn.ipsBanners.insert(json.dumps(nm[host].__dict__))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            gc.collect()

    del pack
    del reply

def scanner_function(i, q):
    print "Thread ", i
    thisThreadConn = MongoConnector()
    icmp = ICMP()

    while True:
        network = q.get()

        ipNet = IPNetwork(network)
        for ip in ipNet:
            scan(thisThreadConn, str(ip), nm, icmp)

        q.task_done()
        del ipNet
        gc.collect()


def main():
    print "Program started"
    sniff(store=0)
    with open('CIDR.txt', 'r') as cidr_file:
        line = cidr_file.readlines()
        for l in line:
            if l.startswith("#"):
                continue
            ipNetworksQueue.put(l)

    for i in xrange(AVAILABLE_THREADS):
        worker = Thread(target=scanner_function, args=(i, ipNetworksQueue))
        worker.setDaemon(True)
        worker.start()

    ipNetworksQueue.join()
    print "Program finished"


if __name__ == '__main__':
    main()
