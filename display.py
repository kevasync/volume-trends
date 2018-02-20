from util import *
import tabulate

intervals = [0, 1, 5, 15, 30, 60, 120, 240, 480, 720, 960, 1440]
db = getCouchDb()

dt = datetime.datetime.now() - datetime.timedelta(seconds=1)
currentPoll = db[getDbIdentifier(dt)]['data']

currentSymbols =  list(map(lambda x: x['symbol'], currentPoll))
volumeBySymbol = dict()

for s in currentSymbols:
	volumeBySymbol[s] =  {}

for i in intervals:
	if i == 0:
		polls = currentPoll
	else:	
		try:
			key = getDbIdentifier(dt - datetime.timedelta(minutes=i))
			polls = db[key]['data']
		except couchdb.http.ResourceNotFound:
			for s in currentSymbols:
				volumeBySymbol[s][i] = '?'
			polls = []
			
	for p in polls:	
		s = p['symbol']
		if s in currentSymbols:
			if i == 0:
				volumeBySymbol[s][i] = float(p['24h_volume_usd'])
			else:
				volumeBySymbol[s][i] = (float(p['24h_volume_usd']) / volumeBySymbol[s][0] - 1) * 100
				#seems to be omitting 1440, may get better at minute granularity
		

reportData = list()
for s in currentSymbols:
	line = ['{} ({})'.format(s, volumeBySymbol[s][0])]
	for i in intervals:
		if i in volumeBySymbol[s]:
			if i != 0:
				line.append(volumeBySymbol[s][i])
		else:
			line.append('?')
	reportData.append(line)		

		
print('change in 24 hour moving volume (time in minutes)')
print(tabulate.tabulate(reportData, headers=['symbol & current', 1, 5, 15, 30, 60, 120, 240, 480, 720, 960, 1440], tablefmt='orgtbl'))
