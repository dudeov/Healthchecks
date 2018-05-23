#!/usr/bin/env python

##
## Junper_PS
## Aleksei Chuvakov
## MegaFon FIFA2018 Network Audit project
## Version #3
##

import paramiko
from west import dict_west
from east import dict_east
import argparse



#######################################################################################

def read_args():

    parser = argparse.ArgumentParser(description='------ Great Description To Be Placed Here ------')
    parser.add_argument('-d', '--device_list', action='store', dest='list', help='A file with the dictionary containing the devices')
    parser.add_argument('-c', '--commands', action='store', dest='my_Command_list', help='List of comand to execute separated by comma')
    parser.add_argument('-f', '--file', action='store', dest='fn', help='This name will be part of the output file')
    parser.add_argument('-a', '--append', action='store_true', help='If we need to append the file, not create a new one', default=False)
    args = parser.parse_args()

    if not args.list or not args.fn or not args.my_Command_list:
        print('Not enough arguments. Try "python ssh-vX -h"')
        print(args.list, args.fn, args.my_Command_list)
        exit()

    if args.list.find('west') != -1:
        devices = dict_west
    elif args.list.find('east') != -1:
        devices = dict_east
    elif args.list.find('test') != -1:
        devices = {'My_vSRX': ('192.168.1.250','High','vSRX')}
    else:
        print('No corresponding device list found')
        exit()
        
    if args.append == True: f_open_flag = 'a'
    else: f_open_flag = 'w'
    UN = 'avbakhmu'
    PW = 'S68Wq**W'

    init_data = {'username': UN, 'password': PW, 'fname': args.fn, 'command_list': args.my_Command_list.split(',')}

    return init_data, devices, f_open_flag

###################################################################################################

def get_info(devices, uname, pword, inp_fname, command_list, f_open_flag):

    paramiko.util.log_to_file("paramiko.log")

    for device in devices:

        fname = devices[device][1] + '_' + inp_fname + "_" + str(device) + '_' + devices[device][2] + ".txt"

        with paramiko.SSHClient() as client:

            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                client.connect(hostname=devices[device][0], username=uname, password=pword)
                print('Connected to {}'.format(device))

            except Exception as var:
                print('Something is wrong with {}: {}\n Going to next loop'.format(device, var))
                continue

            #f_open_flag = 'w'

            for command in command_list:
                stdin, stdout, stderr = client.exec_command(command)
                print(command)
                with open(fname, f_open_flag) as f:
                    f.write('\n{}> {}\n'.format(device, command))
                    f.write(stdout.read())
                    f.write(stderr.read())
                    f.close()
                f_open_flag = 'a'

##################################################################################################

def main():
    (init_data, devices, f_open_flag) = read_args()
    get_info(devices, init_data['username'], init_data['password'], init_data['fname'], init_data['command_list'], f_open_flag)

if __name__ == '__main__':
    main()