from flask import Flask, jsonify
import sqlite3
import json
import time

with open('server.json') as data_file:
    config = json.load(data_file)

def get_cursor():
	conn = sqlite3.connect(config['database_path'])
	c = conn.cursor()

	return (c, conn)

application = Flask(__name__)

@application.route('/')
def spec():

	spec = """<html><body><pre>Interface Specification:

GET /devices

return list of all devices in database.

GET /devices/[timestamp]

return list of all sessions in database with records after [timestamp]

GET /device/[device_name]

return all data for [device_name]

GET /session/[device_name]/latest

return latest data for [device_name]

GET /session/[device_name]/[timestamp]

return all data for [device_name] after [timestamp]
</pre></body></html>
"""

	return spec 

@application.route('/devices', methods=['GET'])

def get_devices():
	(c, conn) = get_cursor()

	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS''')

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@application.route('/devices/<timestamp>', methods=['GET'])

def get_devices_after(timestamp):
	(c, conn) = get_cursor()

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS WHERE TIMESTAMP > ?''',[d])

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@application.route('/device/<device_name>', methods=['GET'])

def get_status(device_name):
	(c, conn) = get_cursor()

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP DESC''', [device_name])

	r = []
	
	for row in c:
		d = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			d[c.description[i][0]] = row[i]
		r.append(d)

	return jsonify(r)

@application.route('/device/<device_name>/latest', methods=['GET'])

def get_status_latest(device_name):
	(c, conn) = get_cursor()

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP DESC LIMIT 1''', [device_name])

	r = {}
	
	for row in c:
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			r[c.description[i][0]] = row[i]

	return jsonify(r)

@application.route('/device/<device_name>/<int:timestamp>', methods=['GET'])

def get_status_after(device_name, timestamp):
	(c, conn) = get_cursor()

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? AND TIMESTAMP > ? ORDER BY TIMESTAMP DESC''', [device_name,d])

	r = []
	
	for row in c:
		d = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			d[c.description[i][0]] = row[i]
		r.append(d)

	return jsonify(r)
	
if __name__ == "__main__":
    application.run()
