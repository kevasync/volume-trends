from util import *
import requests

pollTable = getCouchDbTable('poll')

configPath = getConfigPathFromArgs(sys.argv)
config = getConfig(configPath)

pollInterval = config.get(pollIntervalConfigKey)

while True: 
	data = json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/').content)
	id = getDbIdentifier(datetime.datetime.now())
	writeToTable({'data': data}, pollTable, id)
	print('poll created: {}, sleeping {} seconds'.format(id, pollInterval))
	time.sleep(pollInterval)