#!/bin/python

import getopt
import sqlite3
import sys

def usage():
	#TODO: Write help information
	print "Help!"

def drop_tables(conn):
	c = conn.cursor()
	
	try:
		c.execute('''DROP TABLE SESSION_DATA''')
		c.execute('''DROP TABLE SESSIONS''')
		c.execute('''DROP TABLE DEVICE_STATUS''')
	except:
		pass
		
	try:		
		c.execute('''DROP INDEX SESSION_DATA_IDX ON SESSION_DATA''')
		c.execute('''DROP INDEX SESSIONS_IDX ON SESSIONS''')
		c.execute('''DROP INDEX DEVICE_STATUS_IDX ON DEVICE_STATUS''')
	except:
		pass
	
def create_tables(conn):
	c = conn.cursor()
	
	c.execute('''CREATE TABLE
				SESSION_DATA
				(
					SESSION_ID INTEGER,
					TIMESTAMP TEXT,
					RECORD_TYPE TEXT,
					TOTAL_BYTES INTEGER,
					THROUGHPUT INTEGER,
					JITTER INTEGER,
					ERRORS INTEGER,
					PACKETS_SENT INTEGER,
					PACKET_ERROR_RATE INTEGER,
					PACKETS_OUT_OF_ORDER INTEGER,
					SAMPLE_DURATION INTEGER
				)
				''')

	c.execute('''CREATE TABLE
				SESSIONS
				(
					SESSION_ID INTEGER,
					REMOTE_IP TEXT,
					REMOTE_PORT INTEGER,
					LOCAL_IP TEXT,
					LOCAL_PORT INTEGER,
					BANDWIDTH INTEGER,
					DIRECTION INTEGER,
					START_TIME TEXT,
					DURATION INTEGER,
					LOCAL_PID INTEGER,
					REMOTE_PID INTEGER,
					ENVIRONMENT TEXT,
					COMPLETE INTEGER
				)
				''')
				
	c.execute('''CREATE TABLE
				DEVICE_STATUS
				(
					DEVICE_IP TEXT,
					TIMESTAMP TEXT,
					APN TEXT,
					BAND TEXT,
					CHANNEL INTEGER,
					IMEI INTEGER,
					IMSI INTEGER,
					MME TEXT,
					MME_ID INTEGER,
					PCI INTEGER,
					PLMN TEXT,
					RAT TEXT,
					RSRP REAL,
					SINR REAL,
					SVN INTEGER,
					TAC INTEGER,
					WWAN_IP TEXT,
					CELL_ID INTEGER,
					ENODEB_ID INTEGER
				)
				''')


	c.execute('''CREATE INDEX SESSION_DATA_IDX ON SESSION_DATA (SESSION_ID, TIMESTAMP)''')
	c.execute('''CREATE INDEX SESSIONS_IDX ON SESSIONS (SESSION_ID, LOCAL_IP)''')
	c.execute('''CREATE INDEX DEVICE_STATUS_IDX ON DEVICE_STATUS (DEVICE_IP, TIMESTAMP)''')
				
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:ci", ["help", "output=","clean","initialize"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	
	clean = False
	initialize = False
	output_file = ""
	
	for o, a in opts:
		if o in ("-o", "--output"):
			output_file = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-c", "--clean"):
			clean = True
		elif o in ("-i", "--initialize"):
			initialize = True
		else:
			assert False, "unhandled option"

	if output_file == "":
		usage()
		sys.exit()
	else:
		conn = sqlite3.connect(output_file)
	
	if initialize:
		create_tables(conn)
	if clean:
		drop_tables(conn)
		create_tables(conn)
	
	