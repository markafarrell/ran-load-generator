from flask import Flask, jsonify
import sqlite3
import json
import time
import os

with open('config/server.json') as data_file:
    config = json.load(data_file)

def get_cursor():
	conn = sqlite3.connect(config['database_path'])
	c = conn.cursor()
	return (c, conn)

application = Flask(__name__)

@application.route('/')
def spec():

	spec = """<html><body><pre>Interface Specification:
GET /sessions

return list of all sessions in database. i.e. all unique test ids

GET /sessions/[timestamp]

return list of all sessions in database with records after [timestamp]

GET /session/[session_id]

return all data for [session_id]

GET /session/all

return all data for all sessions

GET /session/[session_id]/[timestamp]

return all data for [session_id] after [timestamp]

GET /session/all/[timestamp]

return all data for all sessions after [timestamp]
</pre></body></html>"""
	return spec 

@application.route('/sessions', methods=['GET'])

def get_sessions():

	(c, conn) = get_cursor()	

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

@application.route('/sessions/<timestamp>', methods=['GET'])

def get_sessions_after(timestamp):

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)

	(c, conn) = get_cursor()	
	
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

@application.route('/session/<session_id>', methods=['GET'])

def get_session_data(session_id):
	
	(c, conn) = get_cursor()	

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
	
	
@application.route('/session/all', methods=['GET'])

def get_all_session_data():
	
	c = get_cursor()	

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

@application.route('/session/<session_id>/<timestamp>', methods=['GET'])

def get_session_data_after(session_id,timestamp):
	(c, conn) = get_cursor()	

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
	
@application.route('/session/all/<timestamp>', methods=['GET'])

def get_all_session_data_after(timestamp):
	(c, conn) = get_cursor()	

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
    application.run()
