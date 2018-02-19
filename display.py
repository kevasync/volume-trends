from util import *

intervals = [1, 5, 15, 30, 60, 120, 240, 480, 720, 960, 1440]
db = getCouchDb()

dt = datetime.datetime.now() - datetime.timedelta(seconds=1)
currentPoll = db[getDbIdentifier(dt)]['data']
currentSymbols =  map(lambda x: x['symbol'], currentPoll)

for i in intervals:
	intervalKey = getDbIdentifier(dt - datetime.timedelta(minutes=i))
	poll = db[getDbIdentifier(dt)]['data']