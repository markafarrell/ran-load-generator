#!/bin/python

import sys
import getopt
import time
from subprocess import Popen, PIPE, check_output, STDOUT
import json
import random
import os
import signal
from datetime import datetime
import sqlite3
import sessionManagement
import threading

def waitToFinish():
	time.sleep(duration+2)
	sessionManagement.kill_test()

def usage():
	help = '''#startSession

##Input:
None

##Output:
iperf results

##flags:
-h: print help

-d: direction (u-Uplink, d-Downlink or b-Bidirectional)

-b: bandwidth (In Mbps)

-r: remote port. If omitted use random port

-l: local port. if omitted use random port

-t: duration in seconds

-o: output type. (sql - insert into sqlite database specified in config/servers.conf)

-i: local interface to use

-e: test enviornment to use (from config/servers.conf)

-s: session id to tag results with

-T: IPv4 TOS

##Purpose:
Start a test session

##Test:
sudo -u www-data python startSession.py -d d -b 10 -t 10 -i 192.168.1.4 -e windsor_production

##Sample Output:

starting iPerf Remote
iPerf Remote started
Starting iPerf Local
2017-02-15 10:29:34,d,1.0,1251600,10012800,0.273,87,981,8.869,0
2017-02-15 10:29:35,d,1.0,1250200,10001600,0.307,0,893,0.000,0
2017-02-15 10:29:36,d,1.0,1250200,10001600,0.679,0,893,0.000,0
2017-02-15 10:29:37,d,1.0,1250200,10001600,0.141,0,893,0.000,0
2017-02-15 10:29:38,d,1.0,1243200,9945600,0.287,0,888,0.000,0
2017-02-15 10:29:39,d,1.0,1255800,10046400,0.367,0,897,0.000,0
2017-02-15 10:29:40,d,1.0,1250200,10001600,1.006,0,893,0.000,0
2017-02-15 10:29:41,d,1.0,1248800,9990400,0.355,0,892,0.000,0
2017-02-15 10:29:42,d,1.0,1244600,9956800,0.399,0,889,0.000,0
Killing Test
Killing csv2filteredcsv
Killing iperf
 Test Complete'''
	print help

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:b:t:i:e:s:r:l:o:T:", ["help", "direction=", "bandwidth=", "time=", "interface=", "environment=", "session", "remote_port=", "local_port=", "output", "TOS="])
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
	sql = False
	remote_port = -1
	local_port = -1
	session = -1
	tos = False

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-d", "--direction"):
			direction = a
		elif o in ("-b", "--bandwidth"):
			try:
				bandwidth = int(a)
			except:
				usage()
				sys.exit()
		elif o in ("-t", "--time"):
			try:
				duration = int(a)
			except:
				usage()
				sys.exit()
		elif o in ("-T", "--TOS"):
			try:
				tos = int(a)
			except:
				usage()
				sys.exit()
		elif o in ("-i", "--interface"):
			interface = a
			#TODO: validate interface
		elif o in ("-l", "--local_port"):
			try:
				local_port = int(a)
			except:
				usage()
				sys.exit()
			#TODO: validate port
		elif o in ("-r", "--remote_port"):
			try:
				remote_port = int(a)
			except:
				usage()
				sys.exit()
			#TODO: validate port
		elif o in ("-e", "--environment"):
			environment_name = a
			try:
				environment = sessionManagement.config['servers'][a]
			except:
				usage()
				sys.exit()
		elif o in ("-s", "--session"):
			session = a
		elif o in ("-o", "--output"):
			if a == "sql":
				sql = True
		else:
			assert False, "unhandled option"

	if direction == 'u' or direction == 'd' or direction == 'b':
		pass
	else:
		usage()
		sys.exit()
		
	if local_port == -1:
		local_port = random.randint(5000,8000)
		
	if remote_port == -1:
		remote_port = random.randint(5000,8000)
		
	datagram_size = 1400

	if session == -1:
		session = random.randint(0,1000000)
	
	sessionManagement.session = session
	sessionManagement.environment = environment
	
	signal.signal(signal.SIGINT, sessionManagement.kill_test)
	
	start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	local_pid = os.getpid()
	
	print "starting iPerf Remote"
	
	remote_pid = sessionManagement.runiPerfRemote(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, tos)
	
	print "iPerf Remote started"
		
	sessionManagement.insertSessionRecord(session, environment_name, environment['hostname'], remote_port, interface, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid)
		
	print "Starting iPerf Local"
	
	timerThread = threading.Thread(target=waitToFinish)
	timerThread.daemon = True
	timerThread.start()
	
	sessionManagement.runiPerfLocal(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, session, tos)
	
	print "Test Complete"
	
	s = sessionManagement.getSession(session)
	
	sessionManagement.killSession(s)	
