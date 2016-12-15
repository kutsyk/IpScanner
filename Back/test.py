#!/usr/bin/python
import nmap
from MyCloud import *

# nm = nmap.PortScanner()
# host = '185.46.221.204'
# nm.scan(host, arguments="--min-rate 1000 --max-retries 0 --min-parallelism 10 -sV -Pn --script=http-title --script=http-headers")
# if nm[host]:
CLIENT.CreateDocument(banners_dev['_self'], {
    'id': 'test_',
    'info': 'test'
})
# print nm[host]
print 'Success'  # else:
#     print 'Fail'
