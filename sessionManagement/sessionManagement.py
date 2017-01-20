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

iperf_process=None
filteredcsv_process=None
csv2sqlite_process=None

session = -1
enviornment = ""

with open('servers.conf') as data_file:
    config = json.load(data_file)
	
conn = sqlite3.connect(config['database_path'])

def kill_test():
	print "Killing Test"
	if csv2sqlite_process != None:
		print "Killing csv2sqlite"
		csv2sqlite_process.terminate()
	if filteredcsv_process != None:
		print "Killing csv2filteredcsv"
		filteredcsv_process.terminate()
	if iperf_process != None:
		print "Killing iperf"
		iperf_process.terminate()
	
	s = getSession(session)
	
	killRemoteSession(session)
	
def runiPerfRemote(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql):
	if direction == 'b':
		test_flag = "-d"
	else:
		test_flag = ""
		
	if(direction == 'd' or direciton == 'b'):
		iperf_command = "iperf -c $SSH_CLIENT -u -i1 -fm -t" + str(duration) + " -b " + str(bandwidth) + "M" + " -l" + str(datagram_size) + " -p" + str(local_port) + " " + str(test_flag) + " -yC > iperf_logs/" + str(session) + " & echo $!"
		ssh_cmd = "ssh\ssh -q -o StrictHostKeyChecking=no -b" + interface + " -o BindAddress=" + interface + " " + environment['username'] + "@" + environment['hostname'] + " -p " + str(environment['ssh_port']) + " -i " + environment['ssh_key'] + " \"" + iperf_command + "\""
		
		remote_pid = check_output(ssh_cmd)
	elif(direction == 'u'):
		pass
	else:
		#TODO: handle incorrect direction
		pass
	
	return remote_pid

def updateLocalPID(session, pid):
	c = conn.cursor()
	c.execute('''UPDATE SESSIONS SET LOCAL_PID = ? WHERE SESSION_ID = ?''', [pid, session])
	conn.commit()
	
def insertSessionRecord(session, environment, remote_ip, remote_port, local_ip, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid):
	conn = sqlite3.connect(config['database_path'])
	c = conn.cursor();
	
	c.execute('''INSERT INTO SESSIONS (SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE)
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (session, remote_ip, remote_port, local_ip, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid, environment, 0))
				
	conn.commit()

def runiPerfLocal(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, session):
	global iperf_process
	global filteredcsv_process
	global csv2sqlite_process
	
	if(direction == 'd' or direciton == 'b'):
		# bufsize=1 means line buffered
		iperf_process = Popen(["iperf\iperf", "-s", "-u", "-i", "1", "-l", str(datagram_size), "-p", str(remote_port), "-y", "C"], stdout=PIPE, bufsize=1)
		filteredcsv_process = Popen(["python", "-u", "../csv2filteredcsv/csv2filteredcsv.py", "-d"], stdin=iperf_process.stdout, stdout=PIPE, bufsize=1)
		iperf_process.stdout.close()
	elif(direction == 'u'):
		pass
	else:
		#TODO: handle incorrect direction
		pass
	
	updateLocalPID(session, iperf_process.pid)
	
	if sql:
		csv2sqlite_process = Popen(["python", "-u", "../csv2sqlite/csv2sqlite.py", "-s", str(session), "-o", config['database_path']], stdin=filteredcsv_process.stdout, stdout=PIPE, bufsize=1)
		filteredcsv_process.stdout.close()
		while csv2sqlite_process.poll() is None:
			try:
				line = csv2sqlite_process.stdout.readline()
				print line,
			except KeyboardInterrupt:
				kill_test()
			except:
				kill_test()
	else:
		while filteredcsv_process.poll() is None:
			try:
				line = filteredcsv_process.stdout.readline()
				print line,
			except KeyboardInterrupt:
				kill_test()
			except:
				kill_test()

def killRemoteSession(session, environment):
	try:
		kill_cmd = "kill -9 " + str(session['REMOTE_PID'])
		ssh_cmd = "ssh\ssh -q -o StrictHostKeyChecking=no -b" + session['LOCAL_IP'] + " -o BindAddress=" + session['LOCAL_IP'] + " " + environment['username'] + "@" + environment['hostname'] + " -p " + str(environment['ssh_port']) + " -i " + environment['ssh_key'] + " \"" + kill_cmd + "\""
		res = check_output(ssh_cmd)
	except:
		res = True
		
	return res
	
def killLocalSession(session):
	return os.kill(session['LOCAL_PID'], signal.SIGTERM)
	
def killSession(session, environment):
	remote_status = killRemoteSession(session, environment)
	local_status = killLocalSession(session)
	
	completeSession(session)
	
def completeSession(session):
	c = conn.cursor()
	c.execute('''UPDATE SESSIONS SET COMPLETE = 1 WHERE SESSION_ID = ?''', [session['SESSION_ID']])
	conn.commit()

def getSession(session):
	c = conn.cursor();
	
	c.execute('''SELECT SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT FROM 
					SESSIONS 
					WHERE SESSION_ID = ?''', [session])

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	return sessions[0]
