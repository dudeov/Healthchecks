#!/usr/bin/env python

import pexpect
import getpass
import re
import time
from devices import *

def upload(dev_uname, dev_pass, dev_address, f_name):
    scp_string = 'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + f_name + ' ' + dev_uname + '@' + dev_address + ':/var/tmp/' + f_name
    with pexpect.spawn(scp_string) as child:
        child.delaybeforesend = .0250
        try:
            child.expect('assword:', timeout=5)
            child.sendline(dev_pass)
            child.expect(f_name + ' +100%')
            print('File copy progerss:\n' + clean_pexpect(child.after))
            return True
        except pexpect.TIMEOUT:
            print("Error!!!\nProblems with scp to %s, Check the address and the password. Next device..." % (dev_address))
            return False
        except Exception as var:
            print("Error!!!\nProblems with scp to %s, error: %s." % (dev_address, var))
            return False

##############   clean pexpect output        ######################

def clean_pexpect(b_str):
    try:
        tmp_str = str(b_str,"utf-8")
    except:
        tmp_str = b_str.decode("utf-8").encode('ascii','ignore')
    str_pretty = re.sub(r'\\r', '', tmp_str)
    return str_pretty

def all_stuff(dev_uname, dev_pass, dev_address_list, f_name = 'Recovery-scriptV15-Active_v2.sh'):

    for dev_address in dev_address_list:
        print(30*'#' + '\n' + "Working on %s"% dev_address)
        bit = upload(dev_uname, dev_pass, dev_address, f_name)
        if not bit:
            continue
        ssh_string = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + dev_uname + '@' + dev_address
        with pexpect.spawn(ssh_string) as child:
            try:
                child.expect('assword:', timeout=15)
                child.sendline(dev_pass)
                user_at = dev_uname + '@'
                child.expect(user_at)
            except Exception as var:
                print("Error!!!\nProblems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue


            try:
                #root pass: Inline123
                child.sendline('configure private')
                child.expect('#')
                child.sendline('set system root-authentication encrypted-password "$1$OHiCLLYW$JvSl6qNkQCSkNIRjfOyw3."')
                child.expect('#')
                child.sendline('commit')
                child.expect('commit complete')
                print('The root password has been changed')
                child.sendline('exit')
                child.expect('>')
            except Exception as var:
                print("Error!!!\nProblems with root password change at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue


            try:
                child.sendline('start shell')
                child.expect('%')
                child.sendline('su')
                child.expect('assword', timeout=15)
                child.sendline('Inline123')
                child.expect('root')
                child.sendline('mkdir /var/tmp/script')
                child.expect('%')
                mv_str = 'cp /var/tmp/' + f_name + ' /var/tmp/script/' + f_name
                child.sendline(mv_str)
                child.expect('%')
                child.sendline('cd /var/tmp/script/')
                child.expect('%')


                child.sendline('ls -la')
                child.expect(f_name)

                child.sendline('\n')
                child.expect('%')

                print("File was successfully copied to /var/tmp/scripts")
            except Exception as var:
                print("Error!!!\nProblems with copying the file at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue

            try:
                child.sendline('ps aux | grep -v grep | grep -w Recovery')
                time.sleep(2)
                child.expect('root ', timeout=4)
                child.sendline('\n')
                child.expect('%')
                str = 'root ' + clean_pexpect(child.before)

                print("The sript has already been started:")
                print(str)
                print("Next device..")

                continue
            except:
                pass


            try:
                start_script_str = 'sh ' + f_name + ' > /var/tmp/script/Script-output.txt &'
                print("Running the line %s"% start_script_str)
                child.sendline(start_script_str)
                child.expect(' \d+\r\n')
                proc_id = int(clean_pexpect(child.after)[1:])
                print("Process id: %s"% proc_id)
            except Exception as var:
                print("Error!!!\nProblems with starting the script at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue



if __name__ == '__main__':
    #un = 'avbakhmu'
    try:
        un = raw_input("Username: ")
    except:
        un = input("Username: ")
    pw = getpass.getpass("Password for %s: " % un)
    all_stuff(un, pw, device_list)