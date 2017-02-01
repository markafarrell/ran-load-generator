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

GET /sessions/[timestamp]

return list of all sessions in database with records after [timestamp]

GET /session/[session_id]

return all data for [session_id]

GET /session/all

return all data for all sessions

GET /session/[session_id]/[timestamp]

return all data for [session_id] after [timestamp]

GET /session/all/[timestamp]

return all data for all sessions after [timestamp]

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
sudo cp config/reportProvider.ini /etc/ran-load-generator/

# Copy init file to /etc/systemd/system
sudo cp config/reportProvider.service /etc/systemd/system/

sudo systemctl start reportProvider
sudo systemctl enable reportProvider

sudo cp config/ran-load-generator.nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/ran-load-generator.nginx.conf /etc/nginx/sites-enabled/

sudo chown -R www-data:www-data /var/www

sudo systemctl reload nginx
