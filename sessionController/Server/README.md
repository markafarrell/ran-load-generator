#sessionControllerServer

##Input:
requests from serverControllerClient

##Output:
HTTP/REST

##flags:
-f: location of sqlite database file. Mandatory

-p: port to listen on

##Purpose:
Allow serverControllerClient to retrieve data about current sessions.

Allow serverControllerClient to start new sessions

Allow serverControllerClient to kill current sessions

##REST Interface Spec:

GET /sessions

return list of all current sessions.

DELETE /session/<test_id>

kill session <test_id>

POST /session/<test_id>

start a new session

FORM contents:
bandwidth=<bandwidth>&duration=<duration>&direction=<uplink|downlink|bi>&remote_port=<remote_port>&local_port=<local_port>&local_interface=<local_interface_ip>&test_server=<windsor_model|windsor_prod|etc>
