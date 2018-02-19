import requests, datetime, json, couchdb, time

base = 'http://localhost:5984'
resource = 'poll'

couchserver = couchdb.Server(base)
if resource in couchserver:
    db = couchserver[resource]
else:
    db = couchserver.create(resource)

while True: 
	dt = datetime.datetime.now()
	id = dt.strftime("%H%M%S")
	data = json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/').content)
	try:
		db[id] = {'data': data}
	except couchdb.http.ResourceConflict: 
		db.delete(db[id])
		db[id] = {'data': data}
	print('data written {}'.format(id))
	time.sleep(.75)