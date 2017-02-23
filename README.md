#csv2filteredcsv

##Input:
Raw csv output of iperf

##Output:
filtered csv 

##flags:

-f: input file. If omitted use stdin as input

-o: output file. Optionally output to a file as well as stdout. 

##Purpose:
Annotate each row with the test id (timestamp of when the test was started)

Annotate each row with the test variables (bandwidth used)

Filter out summary rows

Filter out rows where iperf was acting at the server.

Note: output always goes to stdout regardless if -o is used.

#csv2sqlite

##Input:
filtered csv

##Output:
data inserted into common sqlite database

##flags:
-f: input file. If omitted use stdin as input

-o: output file. Mandatory

-n: initialize a new sqlite database. If output file exists do nothing.

-c: clean. Remove all data from sqlite database referenced by -o

##Purpose:
insert the filtered csv into an sqlite database

#reportProvider

##Input:
requests from reportRetriever for data

##Output:
csv

##flags:
-f: location of sqlite database file. Mandatory

-p: port to listen on

##Purpose:
Allow reportRetriever to retrieve data from the sqlite database via a TCP port.

Allow reportRetriever to determine what tests are current (have data after a set timestamp)

##REST Interface Spec:

GET /sessions

return list of all sessions in database. i.e. all unique test ids

GET /sessions/<timestamp>

return list of all sessions in database with records after <timestamp>

GET /session/<test_id>

return all data for <test_id>

GET /session/<test_id>/<timestamp>

return all data for <test_id> after <timestamp>


#reportRetriever

##Input:
csv data from reportProvider

##Output:
csv (identical to csv2filteredcsv)

##flags:
-h: host to connect to

-p: port to connect to

-s: session id. if omitted output all sessions. If timestamp is included but -s omitted only output sessions that have data after -t.

-t timestamp to get data after.

-o: output file

Note: output always goes to stdout regardless if -o is used.

##Purpose:
Get test data over a TCP port.

#killSession

##Input:
None

##Output:
None

##flags:
-s: session id.

##Purpose:
Kill all the processes associated with a test session.

NOTE: We need a way to kill the remote processes also. Some kind of watchdog/dead-man's switch.

startSession

##Input:
None

##Output:
session id

##flags:
-b: bandwidth

-r: remote port. If omitted use random port

-l: local port. if omitted use random port

-t: duration in seconds

-o: database file. If omitted only output to csv

-i: local interface to use

-s: server IP address

-p: server ssh port

-k: ssh key

-u: ssh username

##Purpose:
Start a test session


#WiFi Access Point

###Install dependancies
~~~~
sudo apt-get install hostapd dnsmasq
~~~~
###Configure dhcpcd to assign static ip address
Add 
~~~~
interface wlan0
static ip_address=172.24.1.1/24
~~~~
to /etc/dhcpcd.conf

###Restart dhcpcd
~~~~
sudo systemctl stop dhcpcd
sudo systemctl start dhcpcd
~~~~
###Restart the wifi interface
~~~~
sudo ifdown wlan0
sudo ifup wlan0
~~~~

###Configure hostapd
~~~~
sudo cp wifi/config/hostapd.conf /etc/hostapd/
~~~~

###Get hostapd to load the configuration on startup
Add
~~~~
DAEMON_CONF="/etc/hostapd/hostapd.conf"
~~~~
to 
/etc/default/hostapd

###Configure DNSmasq
~~~~
sudo cp wifi/config/dnsmasq.conf /etc/

###Configure ip fowarding
Add
~~~~
net.ipv4.ip_forward=1
~~~~
to /etc/sysctl.conf
Enable for the current session
~~~~
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
~~~~

### Start Service
sudo systemctl start hostapd
sudo systemctl enable hostapd
sudo systemctl start dnsmasq
sudo systemctl enable dnsmasq

~~~~
sudo chown dnsmasq:root  /var/lib/misc/dnsmasq.leases
~~~~


