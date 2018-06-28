# How it works:

Run the script:
```
$ python copy_script.py
Username: avbakhmu                     << you will be prompted to provide username and password for the devices
Password for avbakhmu:
##############################
Working on 192.168.1.250               << the script informs you where it's working and on what task
File copy progerss:
Recovery-scriptV15-Active_v2.sh               100%
The root password has been changed
File was successfully copied to /var/tmp/scripts
The sript has already been started:   << checker in case if the shell script has already been started
root      1187  0.0  0.0  1072   336  p0- S     4:01PM   0:00.05 sh Recovery-sc
root@vSRX-test
Next device..
##############################
Working on 10.179.0.102
Error!!!                              << something is wrong!!!
Problems with scp to 10.179.0.102, Check the address and the password. Next device...
##############################
Working on 10.179.0.87
Error!!!
Problems with scp to 10.179.0.87, Check the address and the password. Next device...
##############################
Working on 10.179.0.95
Error!!!
Problems with scp to 10.179.0.95, Check the address and the password. Next device...
NetworkGod:scripts alex.chuvakov$
```
