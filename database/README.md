#databaseManager

##Input:
None

##Output:
sqlite database

##flags:
-o: output file. Mandatory

-i: initialize a new sqlite database. If output file exists do nothing.

-c: clean. Remove all data from sqlite database referenced by -o

##Purpose:
Create a new database file (or clean an existing one) for use with csv2sqlite and other functions.

##Database Schema

Table:
SESSION_DATA

Columns:
-SESSION_ID INTEGER
-TIMESTAMP TEXT
-RECORD_TYPE TEXT
-TOTAL_BYTES INTEGER
-THROUGHPUT INTEGER
-JITTER INTEGER
-ERRORS INTEGER
-PACKETS_SENT INTEGER
-PACKET_ERROR_RATE INTEGER
-PACKETS_OUT_OF_ORDER INTEGER
-SAMPLE_DURATION INTEGER

Table:
SESSIONS

Columns:
- SESSION_ID INTEGER
- REMOTE_IP TEXT
- REMOTE_PORT INTEGER
- LOCAL_IP TEXT
- LOCAL_PORT INTEGER
- BANDWIDTH INTEGER
- DIRECTION INTEGER
- START_TIME TEXT
- DURATION INTEGER
- LOCAL_PID INTEGER
- REMOTE_PID INTEGER
- ENVIRONMENT TEXT
- COMPLETE INTEGER

Table:
DEVICE_STATUS

Columns:

- DEVICE_IP TEXT
- TIMESTAMP TEXT
- APN TEXT
- BAND TEXT
- CHANNEL INTEGER
- IMEI INTEGER
- IMSI INTEGER
- MME TEXT
- MME_ID INTEGER
- PCI INTEGER
- PLMN TEXT
- RAT TEXT
- RSRP REAL
- SINR REAL
- SVN INTEGER
- TAC INTEGER
- WWAN_IP TEXT
- CELL_ID INTEGER
- ENODEB_ID INTEGER

#Installation:

sudo chown pi:www-data database/

sudo chmod g+x database/


