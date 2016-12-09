from cloud import *
from elasticsearch import Elasticsearch

cloud = MongoConnector()
es = Elasticsearch(http_auth=('elastic', 'changeme'))
# TODO: create dynamic index
# TODO: read about search index in mongoDB
# TODO: index documents from mongoDB