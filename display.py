from util import *
import tabulate
from colorama import init
init()

print('% change in 24 hour moving volume (time in minutes)')

pollTable = getCouchDbTable('poll')
volumeChangeTable = getCouchDbTable('volume-ratio')

configPath = getConfigPathFromArgs(sys.argv)
config = getConfig(configPath)
symbolsToDisplay = config.get(symbolsConfigKey)
configIntervals = config.get(intervalsConfigKey)
pollInterval = config.get(pollIntervalConfigKey)
intervals = [0] + configIntervals

sortFunc = lambda x: x
sortColIdx = 0
sortKey = 'market cap'
sortDescending = False
if len(sys.argv) >= 2 :
	sortKey = int(sys.argv[1])
	if sortKey in intervals:
		sortDescending = len(sys.argv) == 3 and sys.argv[2] == '-r'		
		sortColIdx = intervals.index(sortKey)
		sortFunc = lambda x: sorted(x,
			key=lambda k:  getCellFloatVal(k[sortColIdx]),
			reverse=sortDescending)

refreshInterval = pollInterval
while True:
	dt = datetime.datetime.now() - datetime.timedelta(seconds=pollInterval)
	currentPoll = pollTable[getDbIdentifier(dt)]['data']

	currentSymbols = list(map(lambda x: x['symbol'], currentPoll))
	marketCaps = dict()

	for x in currentPoll:
		marketCaps[x['symbol']] = 0
		cap = x['market_cap_usd']
		if cap is not None:
			marketCaps[x['symbol']] = float(cap)

	marketCapMidThreshold = config.get(midCapConfigKey)
	marketCapLargeThreshold = config.get(largeCapConfigKey)

	volumeBySymbol = dict()
	for s in currentSymbols:
		volumeBySymbol[s] =  {}

	for i in intervals:
		if i == 0:
			polls = currentPoll
		else:	
			try:
				key = getDbIdentifier(dt - datetime.timedelta(minutes=i))
				polls = pollTable[key]['data']
			except couchdb.http.ResourceNotFound:
				for s in currentSymbols:
					volumeBySymbol[s][i] = '?'
				polls = []
				
		for p in polls:	
			s = p['symbol']
			if s in currentSymbols:
				vol = p['24h_volume_usd']
				if vol is None:
					volumeBySymbol[s][i] = float(0)
				elif i == 0:
					volumeBySymbol[s][i] = float(vol)
				else:
					try:
						v = (float(vol) / volumeBySymbol[s][0] - 1) * 100
					except:
						v = '?'
					volumeBySymbol[s][i] = v
	

	volRecordId = getDbIdentifier(dt)
	writeToTable(volumeBySymbol, volumeChangeTable, volRecordId)

	reportData = list()
	for s in currentSymbols:
		if marketCaps[s] >= marketCapLargeThreshold:
			color = '32'
		elif marketCaps[s] >= marketCapMidThreshold:
			color = '33'
		else:
			color = '31'

		line = ['\033[2;{};40m{} ({})  \n'.format(color, s, marketCaps[s])]
		for i in intervals:
			if i in volumeBySymbol[s]:
				if i != 0:
					val = volumeBySymbol[s][i]
					line.append(formatCell(val, config))
			else:
				line.append('?')
		if not symbolsToDisplay:
			reportData.append(line)
		elif s in symbolsToDisplay:
			reportData.append(line)
			

	reportData = sortFunc(reportData)
	formattedIntervals = list(map(lambda x: '{}h'.format(x / 60) if x >= 60 else '{}m'.format(x), configIntervals))
	print(tabulate.tabulate(reportData, headers=['symbol & market cap'] + formattedIntervals, tablefmt='orgtbl'))
	print('data above created at {}, sorting by {}{}, refreshing in {} seconds'.format(
		datetime.datetime.now().strftime(gentleDateFormatString),
		'column {}; {} minutes'.format(sortColIdx + 1, sortKey),
		' (descending)' if sortDescending else '',
		refreshInterval))
	
	time.sleep(refreshInterval)
	print('\n\n\n')