#csv2filteredcsv

##Input:
Raw csv output of iperf

##Output:
filtered csv 

##flags:
-i: input file. If omitted use stdin as input
-o: output file. Optionally output to a file as well as stdout. 

##Purpose:
Annotate each row with the test id (timestamp of when the test was started)
Annotate each row with the test variables (bandwidth used)
Filter out summary rows
Filter out rows where iperf was acting at the server.
Note: output always goes to stdout regardless if -o is used.

##Sample:
python csv2filteredcsv.py -i ..\test_data\s_192_168_1_4_2016-11-03-15_24_41_0296.csv
