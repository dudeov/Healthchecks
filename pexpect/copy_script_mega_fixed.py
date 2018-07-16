#!/usr/bin/env python


import pexpect
import getpass
import re
import time
from datetime import datetime

log_time = time.strftime("%d_%b_%Y_%H_%M_%S", time.gmtime())

def create_list_of_d(f_name):
    d_list = []
    try:
        with open(f_name, 'rU') as f:
            for line in f:
                if line[0].isdigit(): d_list.append(line.strip())
    except:
        print('File %s cannot be opened or read, exiting...' % f_name)
        exit()
    print(d_list)
    return d_list



def write_to_log(message, log_f_name = 'script_error_log'):
    try:
        fd = open(log_f_name + '_' + log_time + '.txt' , 'a')
        fd.write('---------------\n#### ERROR ####\n---------------\n%s\n' % message)
        fd.close
    except:
        print("Error log-file is unavailable")

def err_print(message):
    print("--------------\n### ERROR ###\n--------------")
    print(message)
    print("\n")

def get_site_time(start_time):
    end_time = time.strftime("%H:%M:%S", time.gmtime())
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
    print('----\n####\n\nIt took %s to complete this site\n####\n----\n' % tdelta)

def upload(dev_uname, dev_pass, dev_address, f_name):
    scp_string = 'scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + f_name + ' ' + dev_uname + '@' + dev_address + ':/var/tmp/' + f_name
    #print(scp_string)
    with pexpect.spawn(scp_string, dimensions=(200,200)) as child:
        try:
            child.expect('assword:', timeout=3)
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
                err_print("%s SCP error\nCheck the log file for the details." % dev_address)
                write_to_log("%s Import error\nError : '%s" % (dev_address,str(e)))
                return False

        except pexpect.TIMEOUT:
            err_print("Problems with scp to %s, Check the address and the password. Next device..." % (dev_address))
            write_to_log("Problems with scp to %s, Check the address and the password. Next device..." % (dev_address))
            return False
        except Exception as var:
            err_print("Problems with scp to %s, check the log file for the details." % dev_address)
            write_to_log("Problems with scp to %s, error: %s." % (dev_address, var))
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
        start_time = time.strftime("%H:%M:%S", time.gmtime())
        print(30*'#' + '\n' + "Working on %s"% dev_address)

        #Uploading the file
        upload_bit = upload(dev_uname, dev_pass, dev_address, f_name)
        if not upload_bit:
            continue


        ssh_string = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + dev_uname + '@' + dev_address
        with pexpect.spawn(ssh_string, dimensions=(200,200)) as child:
            try:
                child.expect('assword:', timeout=3)
                child.sendline(dev_pass)
                user_at = dev_uname + '@'
                child.expect(user_at)
            except Exception as var:
                err_print("Problems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
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
                err_print("Problems with root password change at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with root password change at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
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
                err_print("Problems with applying the policy at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with applying the policy at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
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
                err_print("%s:Can't get the root privileges: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("%s:Can't get the root privileges: %s. Exiting to next-loop..." % (dev_address, var))
                continue

            # Checking if the script has already been started
            try:
                grep_str = 'ps aux | grep -v grep | grep ' + f_name
                child.sendline(grep_str)
                i = child.expect(['root ', 'root@'])
                if i == 0:
                    out1 = clean_pexpect(child.before) + clean_pexpect(child.after)
                    child.sendline('\n')
                    child.expect('%')
                    err_print("%s: the script has already been started" % dev_address)
                    write_to_log("%s: the script has already been started" % dev_address)
                    print(out1 + clean_pexpect(child.before) + clean_pexpect(child.after))
                    print("Next device..")
                    get_site_time(start_time)
                    continue
                else: pass
            except Exception as var:
                err_print("Some problems at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Some problems at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
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
                child.sendline('pwd')
                child.expect('/var/tmp/script/')
                #vSRX doesn't send EOF, have to catch some string in the output
                child.sendline('ls -la')
                child.expect(f_name)
                out1 = clean_pexpect(child.before) + clean_pexpect(child.after)
                child.sendline('\n')
                child.expect('%')
                print(out1 + clean_pexpect(child.before) + clean_pexpect(child.after))
                print("File was successfully copied to /var/tmp/scripts")
            except Exception as var:
                err_print("Problems with copying the file at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with copying the file at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue


            # Starting the script
            try:
                start_script_str = 'sh ' + f_name + ' &'
                print("######\nRunning the line %s"% start_script_str)
                child.sendline(start_script_str)
                child.expect(' \d+\r\n')
                proc_id = int(clean_pexpect(child.after)[1:])
                print("######\nThe script has been started successfully!")
                print("Process id: %s"% proc_id)
            except Exception as var:
                err_print("Problems with starting the script at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with starting the script at %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                continue

        get_site_time(start_time)


if __name__ == '__main__':

    try:
        un = raw_input("Username: ")
    except:
        un = input("Username: ")



    pw = getpass.getpass("Password for %s: " % un)


    device_list = create_list_of_d('list.txt')
    all_stuff(un, pw, device_list)
