#!/usr/bin/python
from scapy.layers.inet import *

host = '185.15.211.114'
TIMEOUT = 10
pack = IP(dst=host)/ICMP()
reply = sr1(pack, timeout=TIMEOUT)
if reply is None:
    print "Down"
else:
    print "Up"