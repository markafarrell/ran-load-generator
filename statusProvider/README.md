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

GET /devices/<timestamp>

return list of all sessions in database with records after <timestamp>

GET /device/<device_name>

return all data for <device_name>

GET /session/<device_name>/latest

return latest data for <device_name>

GET /session/<device_name>/<timestamp>

return all data for <device_name> after <timestamp>