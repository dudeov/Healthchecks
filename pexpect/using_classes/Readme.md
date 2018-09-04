Here I implemented the class "ssh_expect".

This class has 2 functions: connect and save
- connects does its justice
- send combines sendline and expect; the usage:

d = ssh_expect()
d.connect(un, device, pw)
d.send('show version', 'JUNOS.*')         # <-- define what we want to send and to get in a single line

Error handling hasn't been done yet:

"if self.con_flag == False" should also be in the "connect" funcion, no "disconnect" function as well.
