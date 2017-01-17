#sessionControllerClient

##Input:
None

##Output:
session id

##flags:
-h: host to connect to

-p: port to connect to

-s: session id. Can only be admitted when using -n.

-n: start a new session

-k: kill a session

-b: test bandwidth. Only valid when using -n

-t: test duration. Only valid when using -n

-u: uplink only test. Only valid when using -n

-d: downlink only test. Only valid when using -n

-b: bi-directional test. Only valid when using -n

-r: remote port. If omitted use random port. Only valid when using -n

-l: local port. If omitted use random port. Only valid when using -n

-i: local interface to use

-e : test environment(server) to use.



##Purpose:
Get test data over a TCP port.
