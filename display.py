from util import *
import tabulate
	

intervals = [0, 1, 5, 15, 30, 60, 120, 240, 480, 720, 960, 1440]
db = getCouchDb()

dt = datetime.datetime.now() - datetime.timedelta(seconds=1)
currentPoll = db[getDbIdentifier(dt)]['data']

currentSymbols = list(map(lambda x: x['symbol'], currentPoll))
marketCaps = list(map(lambda x: float(x['market_cap_usd']), currentPoll))
marketCapMin = min(marketCaps) 
marketCapMax = max(marketCaps)
marketCapQuintileInterval = (marketCapMax - marketCapMin) / 5

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
			vol = p['24h_volume_usd']
			if i == 0:
				volumeBySymbol[s][i] = float(vol)
			else:
				volumeBySymbol[s][i] = (float(vol) / volumeBySymbol[s][0] - 1) * 100
				#seems to be omitting 1440, may get better at minute granularity
		

reportData = list()
for s in currentSymbols:
	# todo: color code symbol by market caep quinitile
	line = ['\033[2;37;40m{} ({})  \n'.format(s, volumeBySymbol[s][0])]
	for i in intervals:
		if i in volumeBySymbol[s]:
			if i != 0:
				val = volumeBySymbol[s][i]
				if val != '?':
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
					
					formated = '\033[1;' + color + ';40m {0:.2f}  \n'.format(val)
					line.append(formated)
				else:
					line.append('?')
		else:
			line.append('?')
	reportData.append(line)		

		
print('% change in 24 hour moving volume (time in minutes)')
print(tabulate.tabulate(reportData, headers=['symbol & current', '1m', 5, 15, 30, '1h', 2, 4, 8, 12, 16, 24], tablefmt='orgtbl'))
