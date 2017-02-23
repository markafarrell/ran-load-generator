#startSession

##Input:
None

##Output:
iperf results

##flags:
~~~~
-h: print help

-d: direction (u-Uplink, d-Downlink or b-Bidirectional)

-b: bandwidth (In Mbps)

-r: remote port. If omitted use random port

-l: local port. if omitted use random port

-t: duration in seconds

-o: output type. (sql - insert into sqlite database specified in config/servers.conf)

-i: local interface to use

-e: test enviornment to use (from config/servers.conf)

-s: session id to tag results with
~~~~
##Purpose:
Start a test session

##Test:
~~~~
sudo -u www-data python startSession.py -d d -b 10 -t 10 -i 192.168.1.4 -e windsor_production
~~~~
##Sample Output:
~~~~
starting iPerf Remote
iPerf Remote started
Starting iPerf Local
2017-02-15 10:29:34,d,1.0,1251600,10012800,0.273,87,981,8.869,0
2017-02-15 10:29:35,d,1.0,1250200,10001600,0.307,0,893,0.000,0
2017-02-15 10:29:36,d,1.0,1250200,10001600,0.679,0,893,0.000,0
2017-02-15 10:29:37,d,1.0,1250200,10001600,0.141,0,893,0.000,0
2017-02-15 10:29:38,d,1.0,1243200,9945600,0.287,0,888,0.000,0
2017-02-15 10:29:39,d,1.0,1255800,10046400,0.367,0,897,0.000,0
2017-02-15 10:29:40,d,1.0,1250200,10001600,1.006,0,893,0.000,0
2017-02-15 10:29:41,d,1.0,1248800,9990400,0.355,0,892,0.000,0
2017-02-15 10:29:42,d,1.0,1244600,9956800,0.399,0,889,0.000,0
Killing Test
Killing csv2filteredcsv
Killing iperf
 Test Complete
~~~~

#Installing Service:

###Install Dependancies
~~~~
sudo apt-get install build-essential python-dev python-pip uwsgi uwsgi-plugin-python nginx

sudo pip install flask
~~~~
###Create a directory for the UNIX sockets
~~~~
sudo mkdir /var/run/ran-load-generator
sudo chown www-data:www-data /var/run/ran-load-generator
~~~~
###Create a directory for the logs
~~~~
sudo mkdir /var/log/ran-load-generator
sudo chown www-data:www-data /var/log/ran-load-generator
~~~~
###Create a directory for the configs
~~~~
sudo mkdir /etc/ran-load-generator
~~~~
###Copy config files to /etc/ran-load-generator
~~~~
sudo cp config/sessionService.ini /etc/ran-load-generator/
~~~~
###Copy init file to /etc/systemd/system
~~~~
sudo cp config/sessionService.service /etc/systemd/system/

sudo cp config/ran-load-generator.nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ran-load-generator.nginx.conf /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

sudo chown -R www-data:www-data /var/www

sudo systemctl reload nginx

sudo pip install celery

sudo apt-get install rabbitmq-server

sudo cp config/sessionService-celery.service /etc/systemd/system/
sudo cp config/sessionService-celery.conf /etc/ran-load-generator/

sudo systemctl start sessionService-celery
sudo systemctl enable sessionService-celery
sudo systemctl start sessionService
sudo systemctl enable sessionService

sudo chown www-data:www-data blackbird-key.openssh

sudo systemctl reload nginx
~~~~

###Fix SSH login speed

Edit ssh_config
~~~
sudo nano /etc/ssh/ssh_config
~~~~
Disable GSSAPI authentication
~~~~
#Change 
GSSAPIAuthentication yes
#to
GSSAPIAuthentication no
~~~~
##REST Interface Specification:
~~~~
GET /sessions

return list of all sessions in database. i.e. all unique test ids

GET /sessions/complete

return list of all sessions in database marked complete

GET /sessions/active

return list of all sessions in database that have started by not completed

GET /sessions/[timestamp]

return list of all sessions in database that have results after [timestamp]

GET /sessions/[session_id]

return details of [session_id]

POST /session/

FORM fields:

Required:

-direction : [u/d/b]

-bandwidth : in Mbps

-duration : in seconds

-interface : interface to use for test

-enviornment : environment to test against

Optional:

-datagram-size : in bytes

-remote_port : remote port to be used in test

-local_port : local port to be used in test

GET /environments

return list of configured test environments
~~~~
