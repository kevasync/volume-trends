from util import *
import requests

db = getCouchDb()

while True: 
	data = json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/').content)
	id = getDbIdentifier(datetime.datetime.now())
	try:
		db[id] = {'data': data}
	except couchdb.http.ResourceConflict: 
		db.delete(db[id])
		db[id] = {'data': data}
	print('poll created: {}'.format(id))
	time.sleep(30)