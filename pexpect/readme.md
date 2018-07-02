# Note. Pexpect tricks

```
i = p.expect(['.D-Link.','login:','Username:'])
if i == 0:
    print 'D-Link detected'
    p.expect(['login:','UserName:'])
    p.sendline(login)
    p.expect(['Password:','PassWord'])
    ...
elif i == 1:
    print 'Cisco detected'
    ...
elif i == 2:
    ...


p.interact()    ## интерактивная консоль - отдаем управление пользователю
```

# How the script works:

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
# Note

How to run the shell script manually:
```
start shell
su
cd /var/tmp
mkdir script
cd script
# Paste the script here, under /var/tmp/script
To start: sh script.sh > /var/tmp/script/Script-output.txt &
```
