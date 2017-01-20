#!/bin/python

import getopt
import datetime, threading, time
import sys
import json
import httplib
import pprint

session = ""
host = ""
port = ""
timestamp = None
interval = 1
o = None

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
	return r

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

def get_session_data(session_id):
	# Will return CSV
	conn = httplib.HTTPConnection(host, port)
	conn.request("GET", "/session/" + session_id)
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = ""
	return r
	
def get_session_data_after(session_id,timestamp):
	# Will return CSV
	conn = httplib.HTTPConnection(host, port)
	
	d = time.strftime('%Y%m%d%H%M%S', timestamp)
		
	conn.request("GET", "/session/" + session_id + "/" + d)
	
	response = conn.getresponse()
	
	if(response.status == 200):
		r = response.read()
	else:
		r = ""
	return r

def runGetSessionData():
	global timestamp
	
	next_call = time.time()
	while True:
		#try:
		if timestamp == None:
			r = get_session_data(session)
		else:
			r = get_session_data_after(session, timestamp)
		
		#split respons into rows
		r = r.strip().split('\n')
		
		for row in r:
			res = row.strip().split(',')
			
			try:
				timestamp = time.strptime(res[1], "%Y-%m-%d %H:%M:%S")
				o.write(','.join(res))
				o.write('\n')
			except:
				#Can't parse timestamp, probably a header row
				continue
			
		#except:
			#print "Getting session data failed."
			#TODO: print an error to stderr
		#	pass
			
		next_call = next_call+interval;
		time.sleep(next_call - time.time())

if __name__ == '__main__':
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:s:p:i:o:a:", ["host=", "session=", "port=","interval=","output=","after="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	interval_str = ""
	start_time = ""
	output_file = ""
	
	for o, a in opts:
		if o in ("-s", "--session"):
			session = a
		elif o in ("-h", "--host"):
			host = a
		elif o in ("-p", "--port"):
			port = a
		elif o in ("-o", "--output"):
			output_file = a
		elif o in ("-i", "--interval"):
			interval_str = a
		elif o in ("-a", "--after"):
			start_time = a
		else:
			assert False, "unhandled option"

	if host == "":
		usage()
		sys.exit()
		
	if port == "":
		port = 80
	else:
		try:
			port = int(port)
		except:
			#if specified port is not number exit.
			usage()
			sys.exit()
			
	if output_file == '':
		# No output file specified. Use stdout
		o = sys.stdout
	else:
		o = open(output_file, 'w')
			
	if start_time != "":	
		try:
			#Try to parse input start_time
			timestamp = time.strptime(start_time, "%Y%m%d%H%M%S")
		except:
			#Could not parse the start time. Exit
			usage()
			sys.exit()
	
	if session == "":
		# no session specified. Requesting Session list
		if timestamp == None:
			# Get all sessions
			r = get_sessions()		
			for s in r:
				o.write(json.dumps(s, indent=4, separators=(',', ': ')))
				o.write('\n')
		else:
			# Get sessions with valid data after start time
			r = get_sessions_after(timestamp)	
			for s in r:
				o.write(json.dumps(s, indent=4, separators=(',', ': ')))
				o.write('\n')
	else:
		# Session specified. Requesting Session data
		
		if interval_str == "":
			# No interval specicied. Run a once off
			if timestamp == None:
				o.write(get_session_data(session))
			else:
				o.write(get_session_data_after(session, timestamp))
			
		else:		
			try:
				# Try to parse the input value as a number
				interval = int(interval_str)
				
				timerThread = threading.Thread(target=runGetSessionData)
				timerThread.daemon = True
				timerThread.start()
			except:
				# If it fails default to exit
				usage()
				sys.exit()
		
			while True:
				try:
					time.sleep(0.1)
				except KeyboardInterrupt:
					sys.exit()