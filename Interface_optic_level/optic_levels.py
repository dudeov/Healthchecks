#! /usr/bin/env python

try:
    from lxml import etree
except ImportError:
    print('Failed to import ElementTree from any known place')
    exit()
import re
import datetime as DT
import fn_l


###################################################################################################
def parse_file(fn):
    """
    Parse a file with multiple junos outputs in xml format
    Args: file_to_parse (file): an open file to parse
    Returns: A list of lxml trees with <rpc-reply> root elements
    """
    try:
        file_to_parse = open(fn)
    except:
        print("Unable to open the file:")
        print(fn)
        exit()

    f = open("tmp.xml", 'w')
    # getting rid of everything not related to xml (\n, promts and other crap)
    for line in file_to_parse:
        line1 = line.strip()
        if line1.startswith('</rpc-reply>'):
            f.write(line)
            f.write('\n')
        elif line1.startswith('<'):
            f.write(line)
        else:
            continue
    f.close()
    # File tmp.xml is a clear XML file with set of "rpc-reply" elements


    f = open("tmp.xml")
    list_of_xml_trees = []
    parser = etree.XMLPullParser(events=['end'], recover=True)
    for line in f:
        parser.feed(line)
        for action, element in parser.read_events():
            if (action == 'end') and (element.tag == 'rpc-reply'):
                list_of_xml_trees.append(parser.close())
                parser = etree.XMLPullParser(events=('start', 'end'), recover=True)
    return list_of_xml_trees
    f.close()
    file_to_parse.close()
###################################################################################################


###################################################################################################
def optic_level(rpc_reply_list, fn):
    #print('\n' + '*' * 30 + '\n' + '%s optic Level check' % fn + '\n' + '*' * 30)

    def get_int_status(fn):
        try:
            file_desc = open(fn)
        except:
            print("Unable to open the file:")
            print(fn)
            exit()

        interface_all = file_desc.read()
        #searching for lines with int names and grabbing names+status
        tuples = re.findall(r'([a-z]+-\S+)\s+(\w+)\s+(\w+)', interface_all)
        d = {}
        #converting tuples to dict
        for i in tuples:
            d[i[0]] = (i[1], i[2])
        return d

    d = get_int_status(fn)

    i=0
    #iterrate over all XML trees
    for xml_tree in rpc_reply_list:

        for interface in xml_tree.xpath("//*[local-name() = 'physical-interface']/*[local-name() = 'optics-diagnostics']"):
                try:
                    int_name = interface.getparent()[0].text
                except:
                    continue

                rx, rx_high_warn, rx_low_warn = (None, None, None)

                #print(int_name)
                for statistics in interface:
                    if statistics.tag.find('rx-signal-avg-optical-power') != -1:
                       try:
                        rx = float(statistics.text)
                       except:
                           continue
                    elif statistics.tag.find('laser-rx-power-low-warn-threshold') != -1:
                        try:
                            rx_low_warn = float(statistics.text)
                        except:
                            continue
                    elif statistics.tag.find('laser-rx-power-high-warn-threshold') != -1:
                        try:
                            rx_high_warn = float(statistics.text)
                        except:
                            continue


                if rx and rx_low_warn and rx_high_warn and (rx<rx_low_warn or rx>rx_high_warn):
                    #print("\n%s: RX: %s Low WARNING: %s High WARNING: %s\n" % (int_name, rx, rx_low_warn, rx_high_warn))
                    try:
                        print("%s,%s,%s,%s,%s,%s,%s" % (fn, int_name, rx, rx_low_warn, rx_high_warn,d[int_name][0], d[int_name][1],))
                        i+=1
                    except:
                        continue
    #print("%s optic level issues found" % i)
###################################################################################################


###################################################################################################
def main():
    #save the output to the *.csv file
    list_of_files = fn_l.fn_string.split('\n')
    print("Hostname, Interface, RX, Low WARNING, High Warning, Admin Status, Link Status")
    for fn in list_of_files:
        rpc_reply_list = parse_file(fn)
        optic_level(rpc_reply_list, fn)
###################################################################################################


if __name__ == "__main__":
    main()