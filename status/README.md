#getModemStatus

##Input:
None

##Output:
JSON

##flags:
~~~~
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
~~~~
##Test:
~~~~
python getModemStatus.py -m 192.168.1.1 -p admin
~~~~
#monitorModemStatus

##Input:
None

##Output:
modem status

##flags:
~~~~
-m: Modem IP address. (default 192.168.1.1)

-h: Display help.

-p: Modem admin password (default admin)

-o: Output file (if not specified output to stdout)

-i: Interval between getting modem status

-t: Duration to capture status (seconds)

-c: Output as csv

-j: Output as json

-s: Output to sqlite database
~~~~
##Purpose:
Periodicly retreive status information from the connected modem.

##Sample Output:
~~~~
Timestamp,Device IP,APN,Band,Channel,IMEI,IMSI,MME,MME Id,PCI,PLMN,RAT,RSRP,SINR,SVN,TAC,WWAN_IP,cellId,eNodeBId
2017-02-15 10:18:19,192.168.1.1,telstra.LANES,LTE B3,1275,351588071475585,505720004200015,NHE7,152,263,505-01,LTE,-85,12,01,12290,10.96.197.37,3,530183
2017-02-15 10:18:24,192.168.1.1,telstra.LANES,LTE B3,1275,351588071475585,505720004200015,NHE7,152,263,505-01,LTE,-85,13,01,12290,10.96.197.37,3,530183
2017-02-15 10:18:29,192.168.1.1,telstra.LANES,LTE B3,1275,351588071475585,505720004200015,NHE7,152,263,505-01,LTE,-85,13,01,12290,10.96.197.37,3,530183
~~~~
##Test:
~~~~
python monitorModemStatus.py -i 5 -c
~~~~
#statusProvider

##Input:
REST requests from statusRetriever for data

##Output:
csv or json as per REST Interface Spec

##flags:
~~~~
-o: location of sqlite database file. Mandatory

-p: port to listen on
~~~~
##Purpose:
Allow clients to retrieve data from the sqlite database via HTTP.

##REST Interface Spec:
~~~~
GET /devices

return list of all devices in database.

GET /devices/[timestamp]

return list of all sessions in database with records after [timestamp]

GET /device/[device_name]

return all data for [device_name]

GET /session/[device_name]/latest

return latest data for [device_name]

GET /session/[device_name]/[timestamp]

return all data for [device_name] after [timestamp]
~~~~
Installing:

# Install Dependancies
~~~~
sudo apt-get install build-essential python-dev python-pip uwsgi uwsgi-plugin-python nginx

sudo pip install flask
sudo pip install celery
~~~~
# Create a directory for the UNIX sockets
~~~~
sudo mkdir /var/run/ran-load-generator
sudo chown www-data:www-data /var/run/ran-load-generator
~~~~
# Create a directory for the logs
~~~~
sudo mkdir /var/log/ran-load-generator
sudo chown www-data:www-data /var/log/ran-load-generator
~~~~
# Create a directory for the configs
~~~~
sudo mkdir /etc/ran-load-generator
~~~~
# Copy config files to /etc/ran-load-generator
~~~~
sudo cp config/statusService.ini /etc/ran-load-generator/
~~~~
# Copy init file to /etc/systemd/system
~~~~
sudo cp config/statusService.service /etc/systemd/system/

sudo systemctl start statusService
sudo systemctl enable statusService

sudo cp config/ran-load-generator.nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ran-load-generator.nginx.conf /etc/nginx/sites-enabled/

sudo chown -R www-data:www-data /var/www

sudo systemctl reload nginx

sudo cp config/statusService-celery.service /etc/systemd/system/
sudo cp config/statusService-celery.conf /etc/ran-load-generator/

sudo systemctl start statusService-celery
sudo systemctl enable statusService-celery

~~~~
