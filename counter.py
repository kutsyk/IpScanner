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

docs = list(CLIENT.QueryDocuments(banners_dev['_self'], "Select * from c"))
print len(docs)
