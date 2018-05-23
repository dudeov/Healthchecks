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
def show_task(rpc_reply_list, fn):
    rep_state_str = ""
    #iterrate over all XML trees
    for xml_tree in rpc_reply_list:

        for info_instances in xml_tree.xpath("//*[local-name() = 'software-information']"):
            for info in info_instances:
                if info.tag.find('product-model') != -1:
                    chassis_model = info.text

        rep_state = []
        enable_stat = ''
        for status_instances in xml_tree.xpath("//*[local-name() = 'task-replication-state']"):
            for status in status_instances:
                if status.tag.find('task-gres-state') != -1:
                    enable_stat = status.text
                if status.tag.find('task-protocol-replication-state') != -1:
                    rep_state.append(status.text)

    if ("mx80" not in chassis_model) and ("srx" not in chassis_model) and ("ex" not in chassis_model) and ("qfx" not in chassis_model) and ("m7" not in chassis_model):
        if len(rep_state) == 0:
            rep_state_str = "Status is not available/"
        else:
            for i in rep_state:
                rep_state_str = rep_state_str + str(i) + "/"

        new_rep_str = rep_state_str[0:-1]

        print str(fn) +","+ str(chassis_model) +","+ str(enable_stat) +","+ new_rep_str
###################################################################################################


###################################################################################################
def main():
    list_of_files = fn_l.fn_string.split('\n')
    print("Hostname,Chassis,Enabled\Disabled,Status")
    for fn in list_of_files:
        rpc_reply_list = parse_file(fn)
        show_task(rpc_reply_list, fn)
###################################################################################################


if __name__ == "__main__":
    main()