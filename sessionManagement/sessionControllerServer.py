from flask import Flask, jsonify, request
import sqlite3
import json
import time
import sessionManagement

application = Flask(__name__)

@application.route('/')
def spec():
	spec = """<html><body><pre>Interface Specification:
GET /sessions

return list of all sessions in database. i.e. all unique test ids

GET /sessions/complete

return list of all sessions in database marked complete

GET /sessions/active

return list of all sessions in database that have started by not completed

GET /sessions/[timestamp]

return list of all sessions in database that have results after [timestamp]

GET /sessions/[session_id]

return details of [session_id]

POST /session/

FORM fields:

Required:
-direction : [u/d/b]
-bandwidth : in Mbps
-duration : in seconds
-interface : interface to use for test
-enviornment : environment to test against

Optional:
-datagram-size : in bytes
-remote_port : remote port to be used in test
-local_port : local port to be used in test
</pre></body></html>"""

	return spec

@application.route('/sessions', methods=['GET'])

def get_sessions():
	sessions = sessionManagement.getSessions()
	
	return jsonify(sessions)

@application.route('/sessions/complete', methods=['GET'])
	
def get_sessions_complete():
	sessions = sessionManagement.getSessionsComplete()
	
	return jsonify(sessions)

@application.route('/sessions/active', methods=['GET'])
	
def get_sessions_active():
	sessions = sessionManagement.getSessionsActive()
	
	return jsonify(sessions)
	
@application.route('/sessions/<timestamp>', methods=['GET'])

def get_sessions_after(timestamp):

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
		
	return jsonify(sessionManagement.getSessionsAfter(d))

@application.route('/session/<session_id>', methods=['GET'])

def get_session(session_id):
	return jsonify(sessionManagement.getSession(session_id))
	
@application.route('/session/', methods=['POST'])

def create_session():

	print request.form['environment']

	direction = request.form['direction']
	bandwidth = request.form['bandwidth']
	duration = request.form['duration']
	interface = request.form['interface']
	environment = request.form['environment']
		
	try:
		datagram_size = request.form['datagram_size']
	except:
		datagram_size = 1400
		
	try:
		remote_port = request.form['remote_port']
	except:
		remote_port = random.randint(5000,8000)
	
	try:
		local_port = request.form['local_port']
	except:
		local_port = random.randint(5000,8000)
	
	s = sessionManagement.createSession(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port)

	return str(s)

@application.route('/session/<session_id>', methods=['DELETE'])
	
def terminate_session(session_id):
	s = sessionManagement.getSession(session_id)
	sessionManagement.killSession(s)
	s = sessionManagement.getSession(session_id)
	return jsonify(s)
	
if __name__ == "__main__":
    application.run()
