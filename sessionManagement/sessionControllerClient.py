#!/bin/python

import getopt
import datetime, threading, time
import sys
import json
import httplib
import pprint
import urllib
import random

session = ""
host = ""
port = ""

def usage():
	#TODO: Write help information
	print "Help!"

def get_sessions():
	# Will return JSON List
	conn = httplib.HTTPConnection(host, port)
	conn.request("GET", "/sessions")
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = json.loads(response.read().strip())
	else:
		r = []
	return json.loads(r)

def get_session(session_id):
	# Will return JSON List
	conn = httplib.HTTPConnection(host, port)
	conn.request("GET", "/sessions")
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = json.loads(response.read().strip())
	else:
		r = []
	return json.loads(r)
	
def get_sessions_after(timestamp):
	# Will return JSON List
	conn = httplib.HTTPConnection(host, port)
	d = time.strftime('%Y%m%d%H%M%S', timestamp)
	conn.request("GET", "/sessions/" + d)
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = json.loads(response.read().strip())
	else:
		r = []
	return r

def get_sessions_complete():
	# Will return CSV
	conn = httplib.HTTPConnection(host, port)
	conn.request("GET", "/sessions/complete")
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = ""
	return r

def get_sessions_active():
	# Will return JSON List
	conn = httplib.HTTPConnection(host, port)
	conn.request("GET", "/sessions/active")
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = ""
	return json.loads(r)
	
def create_session(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port):
	# Will return CSV
	conn = httplib.HTTPConnection(host, port)
	
	params = urllib.urlencode({'direction': direction, 'duration': duration, 'interface': interface, 'environment' : environment, 'bandwidth' : bandwidth, 'datagram_size' : datagram_size, 'remote_port' : remote_port, 'local_port' : local_port})
	
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	
	print headers
	
	print params
	
	conn.request("POST", "/session/", params, headers)
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = response.read()
	return r

def kill_session(session):
	# Will return CSV
	conn = httplib.HTTPConnection(host, port)
	
	conn.request("DELETE", "/session/" + session)
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = ""
	return json.loads(r)

if __name__ == '__main__':
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:d:b:t:i:e:r:l:ckp:s:", ["host", "direction=", "bandwidth=", "time=", "interface=", "environment=", "remote_port=", "local_port=", "create", "kill", "port=", "session="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
		
	direction = ""
	bandwidth = -1
	duration = -1
	interface = ""
	environment = ""
	remote_port = -1
	local_port = -1
	kill = False
	create = False
	
	create = False
	
	for o, a in opts:
		if o in ("-h", "--host"):
			host = a
		elif o in ("-p", "--port"):
			port = a
		elif o in ("-s", "--session"):
			session = a
		elif o in ("-d", "--direction"):
			direction = a
			if direction == 'u' or direction == 'd' or direction == 'b':
				pass
			else:
				print "d"
				usage()
				sys.exit()
		elif o in ("-b", "--bandwidth"):
			try:
				bandwidth = int(a)
			except:
				print "b"
				usage()
				sys.exit()
		elif o in ("-t", "--time"):
			try:
				duration = int(a)
			except:
				print "t"
				usage()
				sys.exit()
		elif o in ("-i", "--interface"):
			interface = a
			#TODO: validate interface
		elif o in ("-c", "--create"):
			create = True
		elif o in ("-k", "--kill"):
			kill = True
		elif o in ("-l", "--local_port"):
			try:
				local_port = int(a)
			except:
				print "l"
				usage()
				sys.exit()
			#TODO: validate port
		elif o in ("-r", "--remote_port"):
			try:
				remote_port = int(a)
			except:
				print "r"
				usage()
				sys.exit()
			#TODO: validate port
		elif o in ("-e", "--environment"):
			environment = a
		else:
			assert False, "unhandled option"
	
	if local_port == -1:
		local_port = random.randint(5000,8000)
		
	if remote_port == -1:
		remote_port = random.randint(5000,8000)
		
	datagram_size = 1400
	
	if kill and create:
		#Invalid combination
		print "k and c"
		usage()
		sys.exit()
	
	if session == "":
		# no session specified. Requesting Session list
		
		if kill == True:
			# Session id is mandatory for kill
			usage()
			sys.exit
		elif create == True:
			r = create_session(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port)
			print r
		else:
			# print current sessions
			s = get_sessions_active()
			print json.dumps(s, indent=4, separators=(',', ': '))	
	else:
		# Session specified. kill session
		
		if create == True:
			# Session id is can not be specified for create
			print "c & s"
			usage()
			sys.exit
		
		if kill == True:
			s = kill_session(session)
			print json.dumps(s, indent=4, separators=(',', ': '))
		else:
			s = get_session(session_id)
			print json.dumps(s, indent=4, separators=(',', ': '))