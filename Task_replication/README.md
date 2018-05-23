```show_task.py``` grabs model from ```"show version | display xml"``` and Non-stop routing status from ```"show task replication | display xml"```for a device. If chassis is not MX80 or SRX or QFX, the script shows NSR status for this device.


**Instruction:**
1) Collect ```"show version | display xml,show task replication | display xml"``` from each device and put them into a single file per device
2) Put all filenames in fn_l.py:
```
fn_string = '''Low_SHOW_TASK_KB-PE-CUP-12_MX104.txt
Low_SHOW_TASK_autovo-cr-1-MX240_MX240.txt
Low_SHOW_TASK_spb-ats428-pe1-mx480_MX480.txt
High_SHOW_TASK_KB-P2_MX960.txt'''
```
3) run ```show_task.py > somefile.csv```

The result will be a comma-separated text file that can be opened in Excel
