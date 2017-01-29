from flask import Flask, jsonify, request
import sqlite3
import json
import time
import sessionManagement

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/sessions', methods=['GET'])

def get_sessions():
	sessions = sessionManagement.getSessions()
	
	return jsonify(sessions)

@app.route('/sessions/complete', methods=['GET'])
	
def get_sessions_complete():
	sessions = sessionManagement.getSessionsComplete()
	
	return jsonify(sessions)

@app.route('/sessions/active', methods=['GET'])
	
def get_sessions_active():
	sessions = sessionManagement.getSessionsActive()
	
	return jsonify(sessions)
	
@app.route('/sessions/<timestamp>', methods=['GET'])

def get_sessions_after(timestamp):

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
		
	return jsonify(sessionManagement.getSessionsAfter(d))

@app.route('/session/<session_id>', methods=['GET'])

def get_session(session_id):
	return jsonify(sessionManagement.getSession(session_id))
	
@app.route('/session/', methods=['POST'])

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

@app.route('/session/<session_id>', methods=['DELETE'])
	
def terminate_session(session_id):
	s = sessionManagement.getSession(session_id)
	sessionManagement.killSession(s)
	s = sessionManagement.getSession(session_id)
	return jsonify(s)
	
if __name__ == "__main__":
    app.run()