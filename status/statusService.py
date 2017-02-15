from flask import Flask, jsonify, request, Response
import sqlite3
import json
import time
from getModemStatus import getStatus
from subprocess import Popen
from celery import Celery
from kombu import Queue

with open('config/server.json') as data_file:
    config = json.load(data_file)

def make_celery(app):
        celery = Celery(app.import_name, backend=app.config['result_backend'],
                broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        TaskBase = celery.Task
        class ContextTask(TaskBase):
                abstract = True
                def __call__(self, *args, **kwargs):
                        with app.app_context():
                                return TaskBase.__call__(self, *args, **kwargs)
        celery.Task = ContextTask
        return celery

application = Flask(__name__)

application.config.update(
        CELERY_BROKER_URL='amqp://guest@localhost//',
        result_backend='amqp://guest@localhost//'
)

celery = make_celery(application)

celery.conf.task_routes = {'statusService.*': {'queue': 'statusService'}}

@celery.task(name='statusService.create_device_monitoring_task')
def create_device_monitoring_task(interface, interval, duration):
	start_monitor_process = Popen(["python", "-u", "monitorModemStatus.py", "-m", interface, "-i", str(interval), "-t", str(duration), "-s", "-o", config['database_path']])

def get_cursor():
	conn = sqlite3.connect(config['database_path'])
	c = conn.cursor()

	return (c, conn)

application = Flask(__name__)

@application.route('/')
def spec():

	spec = """<html><body><pre>Interface Specification:

GET /devices

return list of all devices in database.

GET /devices/[timestamp]

return list of all sessions in database with records after [timestamp]

GET /device/[device_name]

return all data for [device_name]

GET /device/[device_name]/latest

return latest data for [device_name]

GET /device/[device_name]/[timestamp]

return all data for [device_name] after [timestamp]

POST /device/[device_name]

FORM fields:

Required:
-interval : in seconds
-duration : in seconds

</pre></body></html>
"""

	return spec 

@application.route('/device/<device_name>', methods=['POST'])

def create_device_recording(device_name):
	try:
		interval = request.form['interval']
	except:
		interval = 5

        duration = request.form['duration']

	create_device_monitoring_task.delay(device_name, interval, duration)	

	return device_name 

@application.route('/devices', methods=['GET'])

def get_devices():
	(c, conn) = get_cursor()

	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS''')

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@application.route('/devices/<timestamp>', methods=['GET'])

def get_devices_after(timestamp):
	(c, conn) = get_cursor()

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)
	
	c.execute('''SELECT DISTINCT DEVICE_IP FROM DEVICE_STATUS WHERE TIMESTAMP > ?''',[d])

	devices = []

	for row in c:
		devices.append(row[0])
		
	return jsonify(devices)

@application.route('/device/<device_name>', methods=['GET'])

def get_status(device_name):
	(c, conn) = get_cursor()

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP ASC''', [device_name])

	r = ""

        #Generate column headers
        for col in c.description:
                r += col[0] + ","

        #remove extra comma and add newline
        r = r[:len(r)-1] + '\n'

        for row in c:
                #join results with comma seperation. Map used to cast each column to string
                r += ','.join(map(str,row)) + '\n'

        return Response(r, mimetype='text/plain')

@application.route('/device/<device_name>/latest', methods=['GET'])

def get_status_latest(device_name):
	(c, conn) = get_cursor()

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? ORDER BY TIMESTAMP DESC LIMIT 1''', [device_name])

	r = {}
	
	for row in c:
		for i in range(0,len(row)):
			# Construct a dictionary using the column headers and results
			r[c.description[i][0]] = row[i]

	return jsonify(r)

@application.route('/device/<device_name>/current', methods=['GET'])

def get_status_current(device_name):
	r = getStatus(device_name, 'admin')

	return jsonify(r)

@application.route('/device/<device_name>/<timestamp>', methods=['GET'])

def get_status_after(device_name, timestamp):
	(c, conn) = get_cursor()

	d = time.strptime(timestamp,'%Y%m%d%H%M%S')
	d = time.strftime('%Y-%m-%d %H:%M:%S', d)

	c.execute('''SELECT * FROM DEVICE_STATUS WHERE DEVICE_IP = ? AND TIMESTAMP > ? ORDER BY TIMESTAMP ASC''', [device_name,d])

	r = ""

        #Generate column headers
        for col in c.description:
                r += col[0] + ","

        #remove extra comma and add newline
        r = r[:len(r)-1] + '\n'

        for row in c:
                #join results with comma seperation. Map used to cast each column to string
                r += ','.join(map(str,row)) + '\n'

        return Response(r, mimetype='text/plain')

if __name__ == "__main__":
    application.run()
