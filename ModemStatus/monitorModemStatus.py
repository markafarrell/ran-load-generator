#!/bin/python

import getModemStatus
import getopt
import datetime, threading, time
import sys
import json
import sqlite3

output_format = ""
sql = False
output_file = ""

def insertModemStatus(output_file,d):
	
	conn = sqlite3.connect(output_file)
	c = conn.cursor();
	
	c.execute('''INSERT INTO DEVICE_STATUS (DEVICE_IP,TIMESTAMP,APN,BAND,CHANNEL,IMEI,IMSI,MME,MME_ID,PCI,PLMN,RAT,RSRP,SINR,SVN,TAC,WWAN_IP,CELL_ID,ENODEB_ID)
				VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (d['LAN_IP'], d['Timestamp'], d['APN'], d['Band'], d['Channel'], d['IMEI'], d['IMSI'], d['MME'], d['MME Id'], d['PCI'], d['PLMN'], d['RAT'], d['RSRP'], d['SINR'], d['SVN'], d['TAC'], d['WWAN_IP'], d['cellId'], d['eNodeBId']))
				
	conn.commit()

def runGetStatus():
	next_call = time.time()
	while True:
		try:
			o = {}
			o = getModemStatus.getStatus(modem_LAN_ip,admin_password)
			if output_format == "json":
				print getModemStatus.generateJSON(o)
			elif output_format == "csv":
				print getModemStatus.generateCSV(o)
			
			else:
				print getModemStatus.generateJSON(o)
				
			
		except:
			#print "Getting status failed."
			#TODO: print an error to stderr
			pass
			
		if sql:
			
			insertModemStatus(output_file,o)
		
		next_call = next_call+interval;
		time.sleep(next_call - time.time())

if __name__ == '__main__':

	admin_password = ''
	modem_LAN_ip = ''
	interval = 1
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:p:i:jcso:", ["help", "modem=", "password=","interval=","json","csv","sql","output"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	interval_str=""
	output_format = "csv"
	
	for o, a in opts:
		if o in ("-m", "--modem"):
			modem_LAN_ip = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-p", "--password"):
			admin_password = a
		elif o in ("-o", "--output"):
			output_file = a
		elif o in ("-i", "--interval"):
			interval_str = a
		elif o in ("-c", "--csv"):
			output_format = "csv"
		elif o in ("-j", "--json"):
			output_format = "json"
		elif o in ("-s", "--sql"):
			sql = True
		else:
			assert False, "unhandled option"

	if admin_password == "":
		# default password is admin
		admin_password = 'admin'

	if modem_LAN_ip == "":
		# default LAN IP is 192.168.1.1
		modem_LAN_ip = '192.168.1.1'
	
	if sql:
		if output_file == "":
			usage()
			sys.exit()
		else:
			conn = sqlite3.connect(output_file)
			#TODO: Handle errors like file not found etc
			
	try:
		# Try to parse the input value as a number
		interval = int(interval_str)
	except:
		# If it fails default to 1
		interval = 1
	
	if output_format == "csv":
		print getModemStatus.generateHeaders()
	
	timerThread = threading.Thread(target=runGetStatus)
	timerThread.daemon = True
	timerThread.start()
	
	while True:
		try:
			time.sleep(0.1)
		except KeyboardInterrupt:
			sys.exit()