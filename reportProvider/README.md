reportProvider

Input:
requests from reportRetriever for data

Output:
csv

flags:
-f: location of sqlite database file. Mandatory
-p: port to listen on

Purpose:
Allow reportRetriever to retrieve data from the sqlite database via a TCP port.
Allow reportRetriever to determine what tests are current (have data after a set timestamp)
REST Interface Spec:
GET /sessions
return list of all sessions in database. i.e. all unique test ids
GET /sessions/<timestamp>
return list of all sessions in database with records after <timestamp>
GET /session/<test_id>
return all data for <test_id>
GET /session/<test_id>/<timestamp>
return all data for <test_id> after <timestamp>
