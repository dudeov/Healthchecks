#!/usr/bin/env python

import pexpect
import getpass
import re
from devices import *

def upload(dev_uname, dev_pass, dev_address, f_name, p_logfile):
    scp_string = 'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + f_name + ' ' + dev_uname + '@' + dev_address + ':/var/tmp/' + f_name
    print(scp_string)
    with pexpect.spawn(scp_string, dimensions=(200,200)) as child:
        try:
            # Open mode a+b(bytes), because pexpect writes in bytes
            child.logfile = open(p_logfile, "ab")
        except Exception as e:
            child.logfile = None

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
                    return False
            except Exception as e:
                print("Import error, error : '%s'" % str(e))
                return False

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

def all_stuff(dev_uname, dev_pass, dev_address_list, f_name = 'Recovery-scriptV15-Active_v2.sh', p_logfile = "pexpect_logfile.txt"):

    for dev_address in dev_address_list:
        print(30*'#' + '\n' + "Working on %s"% dev_address)

        #Uploading the file
        upload_bit = upload(dev_uname, dev_pass, dev_address, f_name, p_logfile)
        if not upload_bit:
            continue


        ssh_string = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + dev_uname + '@' + dev_address
        with pexpect.spawn(ssh_string, dimensions=(200,200)) as child:
            try:
                child.logfile = open(p_logfile, "ab")
            except Exception as e:
                child.logfile = None

            try:
                child.expect('assword:', timeout=15)
                child.sendline(dev_pass)
                user_at = dev_uname + '@'
                child.expect(user_at)
            except Exception as var:
                print("Error!!!\nProblems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue

            # Changing the root password
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


            # Adding the event-policy
            try:
                child.sendline('configure private')
                child.expect('#')
                child.sendline('set event-options policy FEB_restart_trap events system')
                child.expect('#')
                child.sendline('set event-options policy FEB_restart_trap attributes-match system.message matches "DMA issue occurred, FEB automatically restarted"')
                child.expect('#')
                child.sendline('set event-options policy FEB_restart_trap then priority-override severity critical')
                child.expect('#')
                child.sendline('set event-options policy FEB_restart_trap then raise-trap')
                child.expect('#')
                child.sendline('commit')
                child.expect('commit complete')
                print('The event-policy has been configured')
                child.sendline('exit')
                child.expect('>')
            except Exception as var:
                print("Error!!!\nProblems with applying the policy at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue

            # Becoming root in the shell
            try:
                child.sendline('start shell')
                child.expect('%')
                child.sendline('su')
                child.expect('assword', timeout=15)
                child.sendline('Inline123')
                child.expect('root')
                print("We are root!")
            except Exception as var:
                print("Error!!!\nCn't get the root privileges. Exiting to next-loop..." % (dev_address, var))
                continue


            # Moving the file and creating the directory
            try:
                child.sendline('mkdir /var/tmp/script')
                child.expect('%')
                mv_str = 'cp /var/tmp/' + f_name + ' /var/tmp/script/' + f_name
                child.sendline(mv_str)
                child.expect('%')
                child.sendline('cd /var/tmp/script/')
                child.expect('%')
                #vSRX doesn't send EOF, have to catch some string in the output
                child.sendline('ls -la')
                child.expect(f_name)
                out1 = clean_pexpect(child.before) + clean_pexpect(child.after)
                child.sendline('\n')
                child.expect('%')
                print(out1 + clean_pexpect(child.before) + clean_pexpect(child.after))
                print("File was successfully copied to /var/tmp/scripts")
            except Exception as var:
                print("Error!!!\nProblems with copying the file at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue



            # Checking if the script has already been started
            try:
                grep_str = 'ps aux | grep -v grep | grep ' + f_name
                child.sendline(grep_str)
                child.expect('root ', timeout=5)
                out1 = clean_pexpect(child.before) + clean_pexpect(child.after)
                child.sendline('\n')
                child.expect('%')
                print("The sript has already been started:")
                print(out1 + clean_pexpect(child.before) + clean_pexpect(child.after))
                print("Next device..")
                continue
            except:
                pass

            # Starting the script
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
    try:
        un = raw_input("Username: ")
    except:
        un = input("Username: ")

    pw = getpass.getpass("Password for %s: " % un)

    all_stuff(un, pw, device_list)