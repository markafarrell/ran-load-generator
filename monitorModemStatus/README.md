#monitorModemStatus

##Input:
json data from getModemStatus

##Output:
Insert data into SQL database

##flags:
-o: output file. Mandatory

-d: device identifier

-i: interval in seconds between samples

##Purpose:
Periodicly call getModemStatus and insert the results into a sqlite database
