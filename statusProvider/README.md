#statusProvider

##Input:
requests from statusRetriever for data

##Output:
csv

##flags:
-f: location of sqlite database file. Mandatory

-p: port to listen on

##Purpose:
Allow statusRetriever to retrieve data from the sqlite database via a TCP port.

##REST Interface Spec:

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

Installing:

# Install Dependancies

sudo apt-get install build-essential python-dev python-pip uswgi uwsgi-plugin-python nginx

sudo pip install flask

# Create a directory for the UNIX sockets
sudo mkdir /var/run/ran-load-generator
sudo chown www-data:www-data /var/run/ran-load-generator

# Create a directory for the logs
sudo mkdir /var/log/ran-load-generator
sudo chown www-data:www-data /var/log/ran-load-generator

# Create a directory for the configs
sudo mkdir /etc/ran-load-generator

# Copy config files to /etc/ran-load-generator
sudo cp config/statusProvider.ini /etc/ran-load-generator/

# Copy init file to /etc/systemd/system
sudo cp config/statusProvider.service /etc/systemd/system/

sudo systemctl start statusProvider
sudo systemctl enable statusProvider

sudo cp config/ran-load-generator.nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ran-load-generator.nginx.conf /etc/nginx/sites-enabled/

sudo chown -R www-data:www-data /var/www

sudo systemctl reload nginx

