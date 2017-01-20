from flask import Flask, jsonify
import sqlite3
import json
import time

with open('server.json') as data_file:
    config = json.load(data_file)

conn = sqlite3.connect(config['database_path'])
c = conn.cursor()

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/devices', methods=['GET'])

def get_devices():
	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS''')

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@app.route('/devices/<timestamp>', methods=['GET'])

def get_devices_after(timestamp):

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS WHERE TIMESTAMP > ?''',[d])

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@app.route('/device/<device_name>', methods=['GET'])

def get_status(device_name):
	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP DESC''', [device_name])

	r = []
	
	for row in c:
		d = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			d[c.description[i][0]] = row[i]
		r.append(d)

	return jsonify(r)

@app.route('/device/<device_name>/latest', methods=['GET'])

def get_status_latest(device_name):
	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP DESC LIMIT 1''', [device_name])

	r = {}
	
	for row in c:
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			r[c.description[i][0]] = row[i]

	return jsonify(r)

@app.route('/device/<device_name>/<int:timestamp>', methods=['GET'])

def get_status_after(device_name, timestamp):
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
    app.run()