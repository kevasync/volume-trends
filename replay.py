from util import *

configPath = getConfigPathFromArgs(sys.argv)
config = getConfig(configPath)
intervals = config.get(intervalsConfigKey)
replayTable = getCouchDbTable('volume-ratio')

symbols = sys.argv[1].split(',')
start = int(sys.argv[2])
end = int(sys.argv[3])
skipInterval = int(sys.argv[4]) #in minutes

idx = start
while idx <= end:
	try:
		data = replayTable['{}'.format(idx)]
		for s in symbols:
			if s in data:
				symbolData = data[s]
				for i in intervals:
					k = '{}'.format(i)
					if k in symbolData:
						val = symbolData[k]
						if val != '?':
							print('{} - {} - {}: {}'.format(dbIdentifierToGentleString(idx), s, i, float(val)))
							
	except couchdb.http.ResourceNotFound:
		print('data not found: {}'.format(idx))
	idx += skipInterval

