#!/usr/bin/python
import nmap

nm = nmap.PortScanner()

host = '185.15.211.114'
nm.scan(host)
if nm[host]:
    print nm[host]
