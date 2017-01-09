#!/bin/python

import sys
import getopt
import time

def usage():
	#TODO: Write help information
	print "Help!"

input_file = ''
output_file = ''
	
try:
	opts, args = getopt.getopt(sys.argv[1:], "hf:o:", ["help", "file=", "output="])
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
		
for line in i:
	res = line.split(',')
	
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
		
		if interval_sec > 1:
			# Exclude test summary reports
			pass
		else:
			o.write(','.join(res))