#!/usr/bin/python
import sys
import nmap
from cloud import *

cloud = Cloud()

args = sys.argv
if len(args) == 1:
    docs = list(cloud.CLIENT.QueryDocuments(cloud.banners['_self'], "Select * from c"))
elif args[1]:
    docs = list(cloud.CLIENT.QueryDocuments(cloud.banners_dev['_self'], "Select * from c"))
print len(docs)
