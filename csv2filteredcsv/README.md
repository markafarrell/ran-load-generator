#csv2filteredcsv

##Input:
Raw csv output of iperf

##Output:
filtered csv 

##flags:
~~~~
-f: input file. If omitted use stdin as input
-o: output file. Optionally output to a file as well as stdout.
-h: Show help.
-c: Print column labels (Default on)
-u: Mark as uplink results
-d: Mark as downlink results
~~~~
##Purpose:
Annotate each row with the test id (timestamp of when the test was started)
Annotate each row with the test variables (bandwidth used)
Filter out summary rows
Filter out rows where iperf was acting at the server.
Note: output always goes to stdout regardless if -o is used.

##Sample:
~~~~
python csv2filteredcsv.py -f ..\test_data\s_192_168_1_4_2016-11-03-15_24_41_0296.csv  
~~~~
##Output Columns:

- Timestamp
- Record Type
- Sample Duration
- Total Bytes
- Throughput
- Jitter
- Errors
- Packets Sent
- Packet Error Rate
- Packets Out Of Order
