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
to /etc/default/hostapd

###Configure DNSmasq

~~~~
sudo cp wifi/config/dnsmasq.conf /etc/
sudo chown dnsmasq:root  /var/lib/misc/dnsmasq.leases
~~~~

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
~~~~
sudo systemctl start hostapd
sudo systemctl enable hostapd
sudo systemctl start dnsmasq
sudo systemctl enable dnsmasq
~~~~

###Disable Power Save for WiFi
Add 
~~~~
wireless-power off
~~~~
under 
~~~~
iface wlan0 inet manual
~~~~
in /etc/network/interfaces

###Fix DNSMASQ startup file


Add
~~~~
Restart=on-failure
RestartSec=5
~~~~
at the bottom of the [Service] section  of /lib/systemd/system/dnsmasq.service

Add
~~~~
Requires=sys-subsystem-net-devices-wlan0.device
After=sys-subsystem-net-devices-wlan0.device
Wants=sys-subsystem-net-devices-wlan0.device
~~~~
in the [Unit] section of /lib/systemd/system/dnsmasq.service

