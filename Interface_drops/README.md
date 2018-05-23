int-errors.py grabs Input Errors and Output Drops from several outputs of "show interfaces extensive | display xml" for a device, calculates the delta between first and last outputs and if delata is not 0 (errors or drops are incrementing) shows the statistics in comma-separated manner.


Instructions
1) Collect several "show interfaces extensive | display xml" from each device and put them into a single file per device
2) Put all filenames in fn_l.py:
	fn_string = '''High_SHOW_INT_XML_Stack-M9-PE2_MX960.txt
	High_SHOW_INT_XML_M9-Stack-PE1_MX960.txt
	High_SHOW_INT_XML_M9-Stack-PE2_MX960.txt
	...
3) run int-errors.py > somefile.csv

The result will be a comma-separated text file that can be opened in Excel
