#reportRetriever

##Input:
csv data from reportProvider

##Output:
csv (identical to csv2filteredcsv)

##flags:
-h: host to connect to

-p: port to connect to

-s: session id. if omitted output all sessions. If timestamp is included but -s omitted only output sessions that have data after -t.

-t timestamp to get data after.

-o: output file

Note: output always goes to stdout regardless if -o is used.

##Purpose:
Get test data over a TCP port.
