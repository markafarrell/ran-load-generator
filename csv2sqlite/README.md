#csv2sqlite

##Input:
filtered csv

##Output:
data inserted into common sqlite database

##flags:
~~~~
-f: input file. If omitted use stdin as input

-o: output file. Mandatory

-s: session id to tag results with.

-h: display help information
~~~~
##Purpose:
insert the filtered csv into an sqlite database

##Output Columns:

- SESSION_ID
- TIMESTAMP
- RECORD_TYPE
- SAMPLE_DURATION
- TOTAL_BYTES
- THROUGHPUT
- JITTER
- ERRORS
- PACKETS_SENT
- PACKET_ERROR_RATE
- PACKETS_OUT_OF_ORDER
