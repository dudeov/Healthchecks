python ssh-v4.py takes devices from dictionaries like:
```
dict_east = {
'ADL-MX240-BBR-184_re0': ('10.23.255.184','High','MX240'),
'ADL-MX240-BBR-185_re0': ('10.23.255.185','High','MX240'),
'AKS-MX960-BBR-16_re0': ('10.161.255.16','High','MX960'),
'AKS-MX960-BBR-17_re0': ('10.161.255.17','High','MX960'),
'KRD-MX480-BGW-87_re0': ('10.23.255.87','High','MX480')
}
```
Dictionaries are located in east.py and west.py

Options:
-d: east/west/test- from which dictionary we need to extract the list of the devices: dict_west in west.py or dict_east from east.py. That needs to be removed, only this project relate; test - means one vSRX on VirtualBoxd
-c: comma-separated list of commands in ""
-f: filename, each device will have its own separate filename
-a: by default the script creates a new file or overwrite the existing (if one), this option tells script to append the output to the existing file, not re-create
 

**Example:**
```
$ python ssh-v4.py -c 'show chassis routing-egine | display xml,show version | display xml,show task replication | display xml' -f SHOW_TASK -d east
Connected to SMR-IRR-1_re0
show chassis routing-egine | display xml
show version | display xml
show task replication | display xml
Connected to SMR-SNG227-EX2
show chassis routing-egine | display xml
show version | display xml
show task replication | display xml
Connected to SRN-BHM114-19-SIG03
show chassis routing-egine | display xml
show version | display xml
show task replication | display xml
Connected to SRN-BHM114-17-R-SIG01
show chassis routing-egine | display xml
show version | display xml
show task replication | display xml
Connected to SMR-COD1634-23-R-SIG01
show chassis routing-egine | display xml
...
```
