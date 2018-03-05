import datetime, json, couchdb, time, sys, re

pollIntervalConfigKey = "pollInterval"
symbolsConfigKey = "symbols"
largeCapConfigKey = "largeMarketCapThreshold"
midCapConfigKey = "midMarketCapThreshold"
intervalsConfigKey = "intervalsInMinutes"
cellFormatConfigKey = "volChangePercentThresholds"
dtIdxFormatString = '%y%m%d%H%M'
gentleDateFormatString = '%b %d %H:%M'

def getConfig(path):
	j = json.load(open(path))
	config = dict()	
	config[pollIntervalConfigKey] = j.get("pollInternvalInSeconds")
	config[symbolsConfigKey] = j.get("symbolsToDisplay")
	config[largeCapConfigKey] = j.get("largeMarketCapThreshold")
	config[midCapConfigKey] = j.get("midMarketCapThreshold")
	config[intervalsConfigKey] = j.get("intervalsInMinutes")
	config[cellFormatConfigKey] = j.get("volChangeFormatThresholds")
	return config

def getCouchDbTable(resource):
	base = 'http://localhost:5984'
	couchserver = couchdb.Server(base)
	if resource in couchserver:
	    return couchserver[resource]
	else:
	    return couchserver.create(resource)

def getDbIdentifier(dt):
	return dt.strftime(dtIdxFormatString)

def dbIdentifierToGentleString(id):
	dt = datetime.datetime.strptime('{}'.format(id), dtIdxFormatString)
	return dt.strftime(gentleDateFormatString)

def formatCell(val, config):
	if val == '?':
		return val
	else:
		thresholds = config.get(cellFormatConfigKey)
		if val <= thresholds[0]:
			color = '31'
		elif val <= thresholds[1]:
			color = '33'
		elif val >= thresholds[3]:
			color = '32'
		elif val >= thresholds[2]:
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

def getConfigPathFromArgs(args):
	configPath = 'config.json'
	for a in args:
		if a.startswith('-c'):
			configPath = a.split('=')[1] 
	return configPath

def writeToTable(data, table, id):
	try:
		table[id] = data
	except couchdb.http.ResourceConflict: 
		table.delete(table[id])
		table[id] = data
