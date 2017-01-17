#statusRetriever

##Input:
csv data from statusProvider

##Output:
csv

##flags:
-h: host to connect to

-p: port to connect to

-d: device. if omitted output all devices. If timestamp is included but -d omitted only output sessions that have data after -t.

-t: timestamp to get data after.

-l: only output latest data.

-o: output file

Note: output always goes to stdout regardless if -o is used.

##Purpose:
Get test data over a TCP port.
