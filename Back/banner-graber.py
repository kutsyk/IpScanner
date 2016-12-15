#!/usr/bin/python
import nmap
import socket
from netaddr import *
from MyCloud import *

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 0 -sV -Pn"

def grabBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket
        s.connect((ip, port))
        s.send(b'GET /\n\n')
        banner = s.recv(1024)
        return banner
    except:
        return

def scan(host):
    nm.scan(host, arguments=args)
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                print '-----------------------'
                print port
                print (grabBanner(host, port))
                print '-----------------------'

scan('31.131.19.12')
