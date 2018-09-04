#!/usr/bin/env python


import pexpect
import getpass
import re
import time

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

##############   clean pexpect output        ######################

def clean_pexpect(b_str):
    try:
        tmp_str = str(b_str,"utf-8")
    except:
        tmp_str = b_str.decode("utf-8").encode('ascii','ignore')
    str_pretty = re.sub(r'\\r', '', tmp_str)
    return str_pretty

############# CLASS ######################

class ssh_expect:
    def __init__(self):
        self.con_flag = False
        self.err_flag = False


    def connect(self, dev_uname, dev_address, dev_pass):
        ssh_string = 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ' + dev_uname + '@' + dev_address

        self.child = pexpect.spawn(ssh_string, dimensions=(200, 200))
        if self.con_flag == False:
            try:
                self.child.expect('assword:', timeout=3)
                self.child.sendline(dev_pass)
                user_at = dev_uname + '@'
                self.child.expect(user_at)
                self.con_flag = True
            except Exception as var:
                err_print("Problems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                write_to_log("Problems with login to %s, error: %s. Exiting to next-loop..." % (dev_address, var))
                self.err_flag = True

    def send(self, send_str, expect_str, timeout=15):
        try:
            self.child.sendline(send_str)
            self.i = self.child.expect(expect_str)
            print(clean_pexpect(self.child.before + self.child.after))
            self.output = self.child.before + self.child.after
        except:
            print("Problem with %s" % send_str)



############################################

if __name__ == '__main__':
    un = 'ch'
    pw = 'ap5bavfm'
    for device in ['192.168.1.249',]:
        d = ssh_expect()
        d.connect(un, device, pw)
        d.send('show version', 'JUNOS.*')
        d.send('start shell', '%')
        d.send('su', 'assword', timeout=5)
        d.send('Inline123', 'root@.*')






#####  THE OUTPUT  #########



vSRX-test> show version 
Hostname: vSRX-test
Model: firefly-perimeter
JUNOS Software Release [12.1X47-D20.7]

ch@vSRX-test> 
start shell 
%
 su
Password
:
root@vSRX-test% 
