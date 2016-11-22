#!/usr/bin/python
import nmap
import pydocumentdb.document_client as document_client

DOCUMENTDB_HOST = 'https://ipstats.documents.azure.com:443/'
DOCUMENTDB_KEY = 'FuRTjt01UVmWS1KRPxkbLxOw7imKhNyHIWluSxZ8rjwZrJSZwJKJUNBYhAzDsiOHk2yKdzv9JhQOuEHWtDhZ4w=='

DOCUMENTDB_COLLECTION = 'host-banners'
DOCUMENTDB_DATABASE = 'dbs/host-banners'

CLIENT = document_client.DocumentClient(DOCUMENTDB_HOST, {'masterKey': DOCUMENTDB_KEY})
DB = list(CLIENT.QueryDatabases("SELECT * FROM root r WHERE r.id='host-banners'"))
DOCUMENTS_COLL = list(CLIENT.ReadCollections(DOCUMENTDB_DATABASE))
banners = DOCUMENTS_COLL[0]
banners_dev = DOCUMENTS_COLL[1]

nm = nmap.PortScanner()
#nmap -O -A -sV -Pn --osscan-limit --script=http-title --script=http-headers -T4 185.46.221.204
host = '185.46.221.204'
nm.scan(host, arguments="--min-rate 1000 --max-retries 0 --min-parallelism 10 -sV -Pn --script=http-title --script=http-headers")
if nm[host]:
    CLIENT.CreateDocument(banners_dev['_self'], {
        'id': 'test_'+host,
        'info': nm[host]
    })
    # print nm[host]
    print 'Success'
else:
    print 'Fail'
