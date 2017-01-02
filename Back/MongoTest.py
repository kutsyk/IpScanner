from MyCloud import *

connectorTest = MongoConnector()
# connectorTest.ipsHosts.insert({"test":"test"})
res = connectorTest.processedIps.count({"_id" : "127.0.0.1"})
print res == 0
res = connectorTest.processedIps.count({"_id" : 520913335})
print res == 0