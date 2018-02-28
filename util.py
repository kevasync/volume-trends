import datetime, json, couchdb, time, sys, re

pollInterval = 30

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

def formatCell(val):
	if val == '?':
		return val
	else:
		if val <= -15:
			color = '31'
		elif val <= -5:
			color = '33'
		elif val >= 15:
			color = '32'
		elif val >= 5:
			color = '36'
		else:
			color = '34'
				
		return '\033[1;' + color + ';40m {0:.2f} \n'.format(val)

def getCellFloatVal(val):
	groups = re.search(';\S+m\s\S+\s', val)
	if groups: 
		v = groups.group(0).split(" ")[1]
		return float(v)
	else:
		return -99999999999
