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

@app.route('/sessions', methods=['GET'])

def get_sessions():
	c.execute('''SELECT SESSIONS.SESSION_ID, MAX(TIMESTAMP) AS TIMESTAMP , REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION FROM 
					SESSION_DATA 
					INNER JOIN 
					SESSIONS 
					ON
					SESSION_DATA.SESSION_ID = SESSIONS.SESSION_ID
					GROUP BY SESSIONS.SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION''')

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	return jsonify(sessions)

@app.route('/sessions/<timestamp>', methods=['GET'])

def get_sessions_after(timestamp):

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT SESSIONS.SESSION_ID, MAX(TIMESTAMP) AS TIMESTAMP , REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION FROM 
					SESSION_DATA 
					INNER JOIN 
					SESSIONS 
					ON
					SESSION_DATA.SESSION_ID = SESSIONS.SESSION_ID
					WHERE TIMESTAMP > ?
					GROUP BY SESSIONS.SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION GROUP BY SESSION_ID''',[d])

	sessions = []

	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)
		
	return jsonify(sessions)

@app.route('/session/<session_id>', methods=['GET'])

def get_session_data(session_id):
	
	c.execute('''SELECT * FROM SESSION_DATA WHERE SESSION_ID = ? ORDER BY TIMESTAMP ASC''', [session_id])

	#r = {}

	#for row in c:
	#	for i in range(0,len(row)):
	#		r[c.description[i][0]] = row[i]

	r = ""
	
	#Generate column headers
	for col in c.description:
		r += col[0] + ","
	
	#remove extra comma and add newline
	r = r[:len(r)-1] + '\n'
	
	for row in c:
		#join results with comma seperation. Map used to cast each column to string
		r += ','.join(map(str,row)) + '\n'
	
	return r
	
	
@app.route('/session/all', methods=['GET'])

def get_all_session_data():
	
	c.execute('''SELECT * FROM SESSION_DATA ORDER BY TIMESTAMP ASC''')

	#r = {}

	#for row in c:
	#	for i in range(0,len(row)):
	#		r[c.description[i][0]] = row[i]

	r = ""
	
	#Generate column headers
	for col in c.description:
		r += col[0] + ","
	
	#remove extra comma and add newline
	r = r[:len(r)-1] + '\n'
	
	for row in c:
		#join results with comma seperation. Map used to cast each column to string
		r += ','.join(map(str,row)) + '\n'
	
	return r

@app.route('/session/<session_id>/<timestamp>', methods=['GET'])

def get_session_data_after(session_id,timestamp):
	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT * FROM SESSION_DATA WHERE SESSION_ID = ? AND TIMESTAMP > ? ORDER BY TIMESTAMP ASC''', [session_id, d])

	#r = {}
	
	#for row in c:
	#	for i in range(0,len(row)):
	#		r[c.description[i][0]] = row[i]

	r = ""
	
	#Generate column headers
	for col in c.description:
		r += col[0] + ","
	
	#remove extra comma and add newline
	r = r[:len(r)-1] + '\n'
	
	for row in c:
		#join results with comma seperation. Map used to cast each column to string
		r += ','.join(map(str,row)) + '\n'
	
	return r
	
@app.route('/session/all/<timestamp>', methods=['GET'])

def get_all_session_data_after(timestamp):
	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT * FROM SESSION_DATA WHERE TIMESTAMP > ? ORDER BY TIMESTAMP ASC''', [d])

	r = ""
	
	#Generate column headers
	for col in c.description:
		r += col[0] + ","
	
	#remove extra comma and add newline
	r = r[:len(r)-1] + '\n'
	
	for row in c:
		#join results with comma seperation. Map used to cast each column to string
		r += ','.join(map(str,row)) + '\n'
	
	return r
	
if __name__ == "__main__":
    app.run()