import requests
from util import *

db = getCouchDb()

while True: 
	dt = datetime.datetime.now()
	id = getDbIdentifier(dt)
	data = json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/').content)
	try:
		db[id] = {'data': data}
	except couchdb.http.ResourceConflict: 
		db.delete(db[id])
		db[id] = {'data': data}
	print('data written {}'.format(id))
	time.sleep(.75)