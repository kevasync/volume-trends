import datetime, json, couchdb, time

def getCouchDb():
	base = 'http://localhost:5984'
	resource = 'poll'
	couchserver = couchdb.Server(base)
	if resource in couchserver:
	    return couchserver[resource]
	else:
	    return couchserver.create(resource)

def getDbIdentifier(dt):
	return dt.strftime("%y%m%d%H%M")