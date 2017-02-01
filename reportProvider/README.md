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
