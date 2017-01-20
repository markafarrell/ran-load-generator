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
		opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "session="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
		
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-s", "--session"):
			session = a
		else:
			assert False, "unhandled option"

	try:
		s = sessionManagement.getSession(session)
		environment = sessionManagement.config['servers'][s['ENVIRONMENT']]
	except:
		usage()
		sys.exit()
	
	sessionManagement.killSession(s, environment)