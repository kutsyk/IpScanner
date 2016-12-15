#!/usr/bin/python
import sys
from MyCloud import *

cloud = MongoConnector()

args = sys.argv
if len(args) == 1:
    print cloud.ipDevBanners.find().count()
elif args[1]:
    print cloud.ipsBanners.find().count()