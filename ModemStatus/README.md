#getModemStatus

##Input:
None

##Output:
JSON

##flags:
-m: Modem IP address.

-h: Display help.

-p: Modem admin password

##Purpose:
Retreive status information from the connected modem.

##Sample Output:

{
    "APN": "telstra.wap",
    "Band": "LTE B7",
    "Channel": 2950,
    "IMEI": "351588070626600",
    "IMSI": "505013438812645",
    "MME": "VXE7",
    "MME Id": 168,
    "PCI": 25,
    "PLMN": "505-01",
    "RAT": "LTE",
    "RSRP": -76,
    "SINR": 30,
    "SVN": "01",
    "TAC": 12290,
    "WWAN_IP": "10.142.228.25",
    "cellId": 0,
    "eNodeBId": 730003
}

##Test:

D:\Users\d384492\Documents\Projects\ran-load-generator\getModemStatus>python getModemStatus.py -m 192.168.1.1 -p admin