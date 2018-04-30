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

with open('config/servers.conf') as data_file:
    config = json.load(data_file)
	
def get_cursor():
	conn = sqlite3.connect(config['database_path'])
	c = conn.cursor()

	return (c, conn)

def getEnvironments():
	return config['servers'].keys()

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
	
def runiPerfRemote(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, tos=False):
	if direction == 'b':
		test_flag = "-d"
	else:
		test_flag = ""
	
	if os.name == "posix":
		ssh_path = "ssh"
	else:
		ssh_path = "ssh\ssh"
	
	if(direction == 'd' or direction == 'b'):
		iperf_command = "iperf-2.0.5 -c $SSH_CLIENT -u -i1 -fm -t" + str(duration) + " -b " + str(bandwidth) + "M" + " -l" + str(datagram_size) + " -p" + str(local_port) + " " + str(test_flag) + " -L" + str(remote_port)
		if tos != False:
			iperf_command += " -S " + str(tos)
		iperf_command += " -yC > iperf_logs/" + str(session) + " & echo $!"
		ssh_cmd = [ ssh_path, "-q", "-o", "StrictHostKeyChecking=no", "-b", interface, "-o", "BindAddress=" + interface, environment['username'] + "@" + environment['hostname'], "-p", str(environment['ssh_port']), "-i", environment['ssh_key'], iperf_command ]
		print ' '.join(ssh_cmd)
		remote_pid = check_output(ssh_cmd)
		#print remote_pid
	elif(direction == 'u'):
		iperf_command = "iperf-2.0.5 -s -u -i1 -fm -t" + str(duration) + " -b " + str(bandwidth) + "M" + " -l" + str(datagram_size) + " -p" + str(remote_port) + " " + str(test_flag)
		if tos != False:
			iperf_command += " -S " + str(tos)
		iperf_command += " -yC > iperf_logs/" + str(session) + " & echo $!"
		ssh_cmd = [ ssh_path, "-q", "-o", "StrictHostKeyChecking=no", "-b", interface, "-o", "BindAddress=" + interface, environment['username'] + "@" + environment['hostname'], "-p", str(environment['ssh_port']), "-i", environment['ssh_key'], iperf_command ]
		remote_pid = check_output(ssh_cmd)
		#print remote_pid
	else:
		#TODO: handle incorrect direction
		pass
	
	return remote_pid

def updateLocalPID(session, pid):
	(c, conn) = get_cursor()

	c.execute('''UPDATE SESSIONS SET LOCAL_PID = ? WHERE SESSION_ID = ?''', [pid, session])
	conn.commit()
	
def insertSessionRecord(session, environment, remote_ip, remote_port, local_ip, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid):
	(c, conn) = get_cursor()
	
	c.execute('''INSERT INTO SESSIONS (SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE)
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (session, remote_ip, remote_port, local_ip, local_port, bandwidth, direction, start_time, duration, local_pid, remote_pid, environment, 0))
				
	conn.commit()

def runiPerfLocal(direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, sql, session, tos=False):
	global iperf_process
	global filteredcsv_process
	global csv2sqlite_process
	
	if direction == 'b':
		test_flag = "-d"
	else:
		test_flag = ""
	
	if os.name == "posix":
		iperf_path = "iperf"
	else:
		iperf_path = "iperf\iperf"
	
	if(direction == 'd' or direction == 'b'):
		# bufsize=1 means line buffered
		command_array =[iperf_path, "-s", "-u", "-i", "1", "-l", str(datagram_size), "-p", str(local_port), "-y", "C", "-f", "m"]

		if tos != False:
			command_array += ["-S", str(tos)]

		print ' '.join(command_array)

		iperf_process = Popen(command_array, stdout=PIPE, bufsize=1)
		filteredcsv_process = Popen(["python", "-u", "../csv2filteredcsv/csv2filteredcsv.py", "-d"], stdin=iperf_process.stdout, stdout=PIPE, bufsize=1)
		iperf_process.stdout.close()
	elif(direction == 'u'):

		command_array = [iperf_path, "-c", environment['hostname'], "-u", "-i", "1", "-l", str(datagram_size), "-p", str(remote_port), "-L", str(local_port), "-y", "C", "-t", str(duration), "-f", "m", "-b", str(bandwidth) + "M", "-L", str(local_port), test_flag]

		if tos != False:
			command_array += ["-S", str(tos)]

		iperf_process = Popen(command_array, stdout=PIPE, bufsize=1)

		filteredcsv_process = Popen(["python", "-u", "../csv2filteredcsv/csv2filteredcsv.py", "-d"], stdin=iperf_process.stdout, stdout=PIPE, bufsize=1)
		iperf_process.stdout.close()
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
	
def killRemoteSession(session):
	if os.name == "posix":
		ssh_path = "ssh"
	else:
		ssh_path = "ssh\ssh"

	try:
		environment = config['servers'][session['ENVIRONMENT']]
		kill_cmd = "kill -9 " + str(session['REMOTE_PID'])
		ssh_cmd = [ ssh_path, "-q", "-o", "StrictHostKeyChecking=no", "-b", session['LOCAL_IP'], "-o", "BindAddress=" + session['LOCAL_IP'], environment['username'] + "@" + environment['hostname'], "-p", str(environment['ssh_port']), "-i", environment['ssh_key'], kill_cmd ]
		res = check_output(ssh_cmd)
	except:
		res = True
		
	return res
	
def killLocalSession(session):
	try:
		os.kill(session['LOCAL_PID'], signal.SIGKILL)
		return 1
	except:
		return 0
	
def killSession(session):
	remote_status = killRemoteSession(session)
	local_status = killLocalSession(session)
	
	completeSession(session)
	
def completeSession(session):
	(c, conn) = get_cursor()

	c.execute('''UPDATE SESSIONS SET COMPLETE = 1 WHERE SESSION_ID = ?''', [session['SESSION_ID']])
	conn.commit()

def getSession(session):
	(c, conn) = get_cursor()

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
	
def getSessions():
	(c, conn) = get_cursor()

	c.execute('''SELECT SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE FROM 
					SESSIONS''')

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	return sessions
	
def getSession(session_id):
	(c, conn) = get_cursor()

	c.execute('''SELECT SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE FROM 
					SESSIONS WHERE SESSION_ID = ?''', [session_id])

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	if len(sessions) > 0:
		return sessions[0]
	else:
		return []
	
def getSessionsComplete():
	(c, conn) = get_cursor()

	c.execute('''SELECT SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE FROM 
					SESSIONS WHERE COMPLETE = 1''')

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	return sessions
	
def getSessionsActive():
	(c, conn) = get_cursor()
	
	c.execute('''SELECT SESSION_ID, REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE FROM 
					SESSIONS WHERE COMPLETE != 1 AND julianday('now','localtime')<julianday(start_time)+duration/(24.0*60*60)''')

	sessions = []
	
	for row in c:
		session = {}
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			session[c.description[i][0]] = row[i]
		sessions.append(session)

	return sessions

def getSessionsAfter(timestamp):
	(c, conn) = get_cursor()
	
	c.execute('''SELECT SESSIONS.SESSION_ID, MAX(TIMESTAMP) AS TIMESTAMP , REMOTE_IP, REMOTE_PORT, LOCAL_IP, LOCAL_PORT, BANDWIDTH, DIRECTION, START_TIME, DURATION, LOCAL_PID, REMOTE_PID, ENVIRONMENT, COMPLETE FROM 
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
	
def createSession(session, direction, bandwidth, duration, interface, environment, datagram_size, remote_port, local_port, tos):
	command_array = ["python", "-u", "startSession.py", "-d", direction, "-b", str(bandwidth), "-t", str(duration), "-i", interface, "-e", environment, "-s", str(session), "-o", "sql"]

	if tos != False:
		command_array += ["-T", str(tos)]

	start_session_process = Popen(command_array)
