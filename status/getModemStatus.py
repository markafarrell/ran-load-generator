#!/bin/python

import urllib
import urllib2
import sys
import json
import random
import re
from cookielib import CookieJar
import getopt
import time
from datetime import datetime

# Convert MME codes to node names

MME_codes = { 16 : 'PARU', 144 : 'NPE9', 8 : 'PARY', 48 : 'NHE8', 152 : 'NHE7', 112 : 'VWE8', 40 : 'VWE9', 168 : 'VXE7', 160 : 'NNE7', 24 : 'VWE7'}

def usage():
	help = '''#getModemStatus

##Input:
None

##Output:
JSON

##flags:
-m: Modem IP address. (default 192.168.1.1)

-h: Display help.

-p: Modem admin password (default admin)

##Purpose:
Retreive status information from the connected modem.

##Sample Output:

{
    "APN": "telstra.wap",
    "Band": "LTE B7",
    "Channel": 2950,
    "IMEI": "351588070626600",
    "IMSI": "505013438812645",
    "MME": "VXE7",
    "MME Id": 168,
    "PCI": 25,
    "PLMN": "505-01",
    "RAT": "LTE",
    "RSRP": -76,
    "SINR": 30,
    "SVN": "01",
    "TAC": 12290,
    "WWAN_IP": "10.142.228.25",
    "cellId": 0,
    "eNodeBId": 730003
}

##Test:

python getModemStatus.py -m 192.168.1.1 -p admin'''

	print help 

def generateHeaders():
	return "Timestamp,Device IP,APN,Band,Channel,IMEI,IMSI,MME,MME Id,PCI,PLMN,RAT,RSRP,SINR,SVN,TAC,WWAN_IP,cellId,eNodeBId"
	
def generateJSON(o):
	return json.dumps(o, sort_keys=True, indent=4, separators=(',', ': '))

def generateCSV(o):
	return o["Timestamp"] + "," + o["LAN_IP"]+ "," + o["APN"] + "," + o["Band"] + "," + str(o["Channel"]) + "," + str(o["IMEI"]) + "," + o["IMSI"] + "," + o["MME"] + "," + str(o["MME Id"]) + "," + str(o["PCI"]) + "," + o["PLMN"] + "," + o["RAT"] + "," + str(o["RSRP"]) + "," + str(o["SINR"]) + "," + o["SVN"] + "," + str(o["TAC"]) + "," + o["WWAN_IP"] + "," + str(o["cellId"]) + "," + str(o["eNodeBId"])

def getStatus(modem_IP, password):
	#TODO: Handle no device connected gracefully
		
	cj = CookieJar()

	#Get cookie and security token

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	a = opener.open("http://" + modem_IP + "/index.html").read()

	# Grab the security token from the HTML 
	# TODO: Get this from the cookie name instead.

	m = re.search('"secToken"\s*:\s*"([\w]+)"', a)

	if m != None:
		tok = m.group(1)

	# Login with security token, cookie and password
		
	post_url = 'http://' + modem_IP + '/Forms/config'
	form_data = {'token': tok, 'ok_redirect': '/index.html', 'err_redirect': '/index.html', 'session.password' : password}
	params = urllib.urlencode(form_data)
	response = opener.open(post_url, params)

	# Actually grab the status data

	f = opener.open("http://" + modem_IP + "/api/model.json?internalapi=1&x=" + str(random.randint(0,1000000)))
	j = json.loads(f.read())

	o = {}

	o['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	o['RAT'] = j['wwan']['currentPSserviceType']

	if o['RAT'] == 'LTE':
		o['PCI'] = j['wwanadv']['primScode']
		o['RSRP'] = j['wwan']['signalStrength']['rsrp']
		o['SINR'] = j['wwan']['signalStrength']['sinr']
		o['MME Id'] = j['wwanadv']['RAC'] 
		o['MME'] = MME_codes[int(j['wwanadv']['RAC'])]
		o['TAC'] = j['wwanadv']['LAC'] 
		o['eNodeBId'] = int(j['wwanadv']['cellId'])/256
		o['cellId'] = int(j['wwanadv']['cellId'])%256
	elif o['RAT'] == 'WCDMA':
		o['PSC'] = j['wwanadv']['primScode']
		o['RSCP'] = j['wwan']['signalStrength']['rscp']
		o['ECIO'] = j['wwan']['signalStrength']['ecio']
		o['LAC'] = j['wwanadv']['LAC'] 
		o['RAC'] = j['wwanadv']['RAC'] 
		
	o['IMEI'] = j['general']['IMEI']
	o['SVN'] = j['general']['SVN']
	o['IMSI'] = j['sim']['imsi']
	o['LAN_IP'] = j['router']['gatewayIP']

	for p in j['wwan']['profileList']:
		if p['index'] == j['wwan']['profile']['default']:
			o['APN'] = p['apn']
			break
			
	o['WWAN_IP'] = j['wwan']['IP']

	o['Band'] = j['wwanadv']['curBand']
	o['PLMN'] = j['wwanadv']['MCC'] + "-" + j['wwanadv']['MNC'] 
	o['Channel'] = j['wwanadv']['chanId'] 

	return o
	
if __name__ == '__main__':
    # getModemStatus.py executed as script
    # do something
	admin_password = ''
	modem_LAN_ip = ''

	# initialise the cookie handling package

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:p:jc", ["help", "modem=", "password=","json","csv"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
		
	for o, a in opts:
		if o in ("-m", "--modem"):
			modem_LAN_ip = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-p", "--password"):
			admin_password = a
		else:
			assert False, "unhandled option"


	if admin_password == "":
		# default password is admin
		admin_password = 'admin'

	if modem_LAN_ip == "":
		# default LAN IP is 192.168.1.1
		modem_LAN_ip = '192.168.1.1'
		
	o = {}
	
	o = getStatus(modem_LAN_ip,admin_password)
	
	print json.dumps(o, sort_keys=True, indent=4, separators=(',', ': '))
