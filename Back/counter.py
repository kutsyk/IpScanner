#!/usr/bin/python
import sys
import nmap
from cloud import *

args = sys.argv
if len(args) == 1:
    docs = list(CLIENT.QueryDocuments(banners['_self'], "Select * from c"))
elif args[1]:
    docs = list(CLIENT.QueryDocuments(banners_dev['_self'], "Select * from c"))
print len(docs)
