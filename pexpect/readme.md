# Note. Pexpect tricks

```
#### Terminal length and width
The dimensions attribute specifies the size of the pseudo-terminal as seen by the subprocess, and is specified
as a two-entry tuple (rows, columns). If this is unspecified, the defaults in ptyprocess will apply.

with pexpect.spawn(ssh_string, dimensions=(200,200)) as child:

Without that I was not able to get a proper screen width, so grep didn't work. The output was:
root      1187  0.0  0.0  1072   336  p0- S     4:01PM   0:00.14 sh Recovery-sc

and full "grep -v Recovery-scriptV15-Active_v2.sh" didn't work, because Recovery-scriptV15-Active_v2.sh != Recovery-sc
                
#### Logging
with pexpect.spawn('some string') as child:
    try:
        child.logfile = open(pexpect_logfile, "a")
    except Exception as e:
        child.logfile = None
        

#### Expect multiple parameters
i = child.expect(['.D-Link.','login:','Username:'])     ## Expect a match from a list of strings
if i == 0:
    print 'D-Link detected'
    child.expect(['login:','UserName:'])
    child.sendline(login)
    child.expect(['Password:','PassWord'])
    ...
elif i == 1:
    print 'Cisco detected'
    ...
elif i == 2:
    ...

#### Virtual console
child.interact()    ## интерактивная консоль - отдаем управление пользователю

            
#### File copy (100%)
with pexpect.spawn('scp file.txt user@host:/var/tmp/file.txt') as child:
    try:
        child.expect('assword:', timeout=5)
        child.sendline(dev_pass)
        try:
            child.expect(pexpect.EOF, timeout=30)
            out = clean_pexpect(child.before)
            print(out)
            if '100%' in out:
                return True
            else:
            ...
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
