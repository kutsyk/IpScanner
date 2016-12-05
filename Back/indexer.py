from cloud import *
from elasticsearch import Elasticsearch

cloud = Cloud()
es = Elasticsearch(http_auth=('elastic', 'changeme'))

docs = list(cloud.CLIENT.QueryDocuments(cloud.banners_dev['_self'], "Select * from c"))
for i, doc in enumerate(docs):
    try:
        res = es.index(index="ipstats", doc_type='banner', id=i, body=doc)
    except:
        print i