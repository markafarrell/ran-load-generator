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

def usage():
	#TODO: Write help information
	print "Help!"

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hd:b:t:i:e:sr:l:", ["help", "direction=", "bandwidth=", "time=", "interface=", "environment=", "sql", "remote_port=", "local_port="])
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
		elif o in ("-s", "--sql"):
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

	session = random.randint(0,1000000)
	
	sessionManagement.session = session
	sessionManagement.environment = environment
	
	signal.signal(signal.SIGINT, sessionManagement.kill_test)
	
	start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	local_pid = os.getpid()
	
	remote_pid = sessionManagement.runiPerfRemote(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql)
	
	sessionManagement.insertSessionRecord(session, environment_name, environment['hostname'], remote_port, interface, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid)
	
	sessionManagement.runiPerfLocal(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, session)
	