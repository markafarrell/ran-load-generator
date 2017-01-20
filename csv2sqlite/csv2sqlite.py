#!/bin/python

import sys
import getopt
import time
import sqlite3
import random

def usage():
	#TODO: Write help information
	print "Help!"

def insertSessionDataRecord(conn, d):
	c = conn.cursor();
	
	c.execute('''INSERT INTO SESSION_DATA (SESSION_ID,TIMESTAMP,RECORD_TYPE,SAMPLE_DURATION,TOTAL_BYTES,THROUGHPUT,JITTER,ERRORS,PACKETS_SENT,PACKET_ERROR_RATE,PACKETS_OUT_OF_ORDER)
				VALUES (?,?,?,?,?,?,?,?,?,?,?)''', d)
				
	sys.stdout.write(','.join(map(str,d)))
	sys.stdout.write('\n')
				
	conn.commit()

def check_database(conn):
	#TODO: Check that the database schema is good
	return True
				
def usage():
	#TODO: Write help information
	print "Help!"

if __name__ == '__main__':

	input_file = ''
	output_file = ''
	session = ''

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:o:s:", ["help", "file=", "output=", "session="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
		
	for o, a in opts:
		if o in ("-f", "--file"):
			input_file = a
		elif o in ("-o", "--output"):
			output_file = a
		elif o in ("-s", "--session"):
			session = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			assert False, "unhandled option"

	if input_file == '':
		# No input file specified. Use stdin
		i = sys.stdin
	else:
		i = open(input_file, 'r')

	if output_file == '':
		usage()
		sys.exit()
	else:
		conn = sqlite3.connect(output_file)
		
	if check_database(conn) == False:
		usage()
		sys.exit()
	
	if session == "":
		session = random.randint(0,1000000)
	else:
		try:
			session=int(session)
		except:
			usage()
			sys.exit()
	
	while True:
		try:
			line = i.readline()
		except KeyboardInterrupt:
			sys.exit()

		if not line: 
			break # EOF
	
		res = line.strip().split(',')
		
		# Check if the line is valid by seeing if the first column is a valid datetime
		
		try:
			dt = time.strptime(res[0],'%Y-%m-%d %H:%M:%S')
			res[0] = time.strftime('%Y-%m-%d %H:%M:%S', dt)
		
			insertSessionDataRecord(conn,[session] + res)
		except:
			# If we can't parse the datetime go onto the next line.
			continue