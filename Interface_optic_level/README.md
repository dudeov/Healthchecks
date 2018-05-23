```optic_levels.py``` grabs interface status from ```"show interfaces terse"``` and optic levels and threshold ```"show interfaces diagnostics optics | display xml"``` for a device, then if RX optic signal above or below the thresholds it show this interface and its status.
Status is needed, because Juniper shows optic levels even for interfaces which are down or even admin down.

**Instruction:**
1) Collect ```"show interfaces terse,show interfaces extensive | display xml"``` from each device and put them into a single file per device
2) Put all filenames in fn_l.py:
```
fn_string = '''High_SHOW_OPTICS_MX-PaCo-2-NiiS_MX960.txt
High_SHOW_OPTICS_RST-MX480-BBR-20_re0_MX480.txt'''.
```
3) run ```optic_levels.py > somefile.csv```
