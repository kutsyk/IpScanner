#!/usr/bin/python
import nmap
from netaddr import *

nm = nmap.PortScanner()
args = "--min-rate 1000 --max-retries 0 -sV -Pn --script=http-title --script=http-headers"


def scan(host):
    nm.scan(hosts=host, arguments=args)
    res = {}
    res["tcp"] = []
    lport = nm[host]["tcp"].keys()
    for port in lport:
        portInfo = { "port" : port }
        for portKey in nm[host]["tcp"][port].keys():
            if portKey == 'script':
                portInfo[portKey] = {}
                for httpKeys in nm[host]["tcp"][port][portKey].keys():
                    portInfo[portKey][httpKeys] = GetPlainString(nm[host]["tcp"][port][portKey][httpKeys])
            else:
                portInfo[portKey] = GetPlainString(nm[host]["tcp"][port][portKey])
        res["tcp"].append(portInfo)
    res["hostnames"] = nm[host]["hostnames"]
    res["addresses"] = nm[host]["addresses"]
    res["vendor"] = nm[host]["vendor"]

def GetPlainString(string):
    return string.replace('\n', ' ').replace('\r', '')
# ipNet = IPNetwork('31.131.16.0/20')
# for ip in ipNet:
#     print ip

scan('31.131.19.12')
