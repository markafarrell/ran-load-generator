#csv2sqlite

##Input:
filtered csv

##Output:
data inserted into common sqlite database

##flags:
-f: input file. If omitted use stdin as input

-o: output file. Mandatory

-n: initialize a new sqlite database. If output file exists do nothing.

-c: clean. Remove all data from sqlite database referenced by -o

##Purpose:
insert the filtered csv into an sqlite database

##Output Columns:

-Session Id
-Timestamp
-Source IP
-Source Port
-Destination IP
-Destination Port
-ID
-Time Interval
-Total Bytes
-Throughput (bps)
-Jitter (ms)
-Errors
-Packets Sent
-Packet Error Rate (%) 
-Packets Out Of Order