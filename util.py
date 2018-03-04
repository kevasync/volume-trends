import datetime, json, couchdb, time, sys, re

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

pollIntervalConfigKey = "pollInterval"
symbolsConfigKey = "symbols"
largeCapConfigKey = "largeMarketCapThreshold"
midCapConfigKey = "midMarketCapThreshold"
intervalsConfigKey = "intervalsInMinutes"

def getConfig(path):
	j = json.load(open(path))
	config = dict()	
	config[pollIntervalConfigKey] = j.get("pollInternvalInSeconds")
	config[symbolsConfigKey] = j.get("symbolsToDisplay")
	config[largeCapConfigKey] = j.get("largeMarketCapThreshold")
	config[midCapConfigKey] = j.get("midMarketCapThreshold")
	config[intervalsConfigKey] = j.get("intervalsInMinutes")
	return config

def getConfigPathFromArgs(args):
	configPath = 'config.json'
	for a in args:
		if a.startswith('-c'):
			configPath = a.split('=')[1] 
	return configPath