#!/bin/python

import sys
import getopt
import time

def generateHeaders():
	return "Timestamp,Record Type,Sample Duration,Total Bytes,Throughput,Jitter,Errors,Packets Sent,Packet Error Rate,Packets Out Of Order"

def usage():
	help = '''#csv2filteredcsv

##Input:
Raw csv output of iperf

##Output:
filtered csv

##flags:
-f: input file. If omitted use stdin as input
-o: output file. Optionally output to a file as well as stdout.
-h: Show help.
-c: Print column labels (Default on)
-u: Mark as uplink results
-d: Mark as downlink results

##Purpose:
Annotate each row with the test id (timestamp of when the test was started)
Annotate each row with the test variables (bandwidth used)
Filter out summary rows
Filter out rows where iperf was acting at the server.
Note: output always goes to stdout regardless if -o is used.

##Sample:
python csv2filteredcsv.py -f ..\test_data\s_192_168_1_4_2016-11-03-15_24_41_0296.csv

##Output Columns:

-Timestamp
-Record Type
-Sample Duration
-Total Bytes
-Throughput
-Jitter
-Errors
-Packets Sent
-Packet Error Rate
-Packets Out Of Order
'''
	print help 

input_file = ''
output_file = ''
columns=False
record_type=""

try:
	opts, args = getopt.getopt(sys.argv[1:], "hf:o:cud", ["help", "file=", "output=", "columns","uplink","downlink"])
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
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-c", "--columns"):
		columns=True
	elif o in ("-u", "--uplink"):
		record_type = 'u'
	elif o in ("-d", "--downlink"):
		record_type = 'd'
	else:
		assert False, "unhandled option"

if input_file == '':
	# No input file specified. Use stdin
	i = sys.stdin
else:
	i = open(input_file, 'r')

if output_file == '':
	# No output file specified. Use stdout
	o = sys.stdout
else:
	o = open(output_file, 'w')

if record_type == '':
	usage()
	sys.exit()
	
if columns:
	o.write(generateHeaders())
	o.write('\n')
	
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
		dt = time.strptime(res[0],'%Y%m%d%H%M%S')
		res[0] = time.strftime('%Y-%m-%d %H:%M:%S', dt)
	except:
		# If we can't parse the datetime go onto the next line.
		continue
	
	if len(res) < 14:
	# Report is not for received data. Throw away
		pass
	else:
		# Get length of interval
		interval = res[6].split('-')
		interval_sec = float(interval[1])-float(interval[0])
		res[6] = str(interval_sec)
		
		if interval_sec > 1:
			# Exclude test summary reports
			pass
		else:
			res = [res[0], record_type] + res[6:]
			try:
				o.write(','.join(res))
				o.write('\n')
			except:
				print res
