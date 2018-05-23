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
    rpc_num = 0

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
            rpc_num += 1
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
    return list_of_xml_trees, rpc_num
    f.close()
    file_to_parse.close()
###################################################################################################


###################################################################################################
def int_errors_delta(rpc_reply_list, rpc_num, fn):
    #print('\n' + '*' * 30 + '\n' + 'Interface check' + '\n' + '*' * 30 + '\n')

    int_dic = {}
    int_bad = {}

    #iterrate over all XML trees
    for xml_tree in rpc_reply_list:

        for interface in xml_tree.xpath("//*[local-name() = 'physical-interface']"):
                try:
                    int_name = interface[0].text
                except:
                    continue

                bpdu_er, l2tp_er, l_fl, tot_drops, tot_out_er, tot_in_er = (None, None, None, None, None, None)

                for statistics in interface:
                    if statistics.tag.find('bpdu-error') != -1:
                        bpdu_er = statistics.text
                        if bpdu_er.find('one') != -1: bpdu_er = 0
                        else: bpdu_er = int(bpdu_er)

                    elif statistics.tag.find('l2pt-error') != -1:
                        l2tp_er = statistics.text
                        if l2tp_er.find('one') != -1: l2tp_er = 0
                        else: l2tp_er = int(l2tp_er)

                    elif re.search(r'interface-flapped', statistics.tag):
                        l_fl = statistics.text
                        if re.search('never', l_fl, re.IGNORECASE): l_fl = 0
                        elif re.search('(\d+:\d+:\d+)\s+(ago)', l_fl, re.IGNORECASE):
                            ts1 = re.search('(\d+:\d+:\d+)\s+(ago)', l_fl, re.IGNORECASE).group(1)
                            t1 = DT.datetime.strptime(ts1, '%H:%M:%S')
                            t2 = DT.datetime(1900, 1, 1)
                            l_fl = int((t1 - t2).total_seconds()/60)
                        else: l_fl = None


                    elif statistics.tag.find('input-error-list') != -1:
                        inp_er_l = []

                        for inp_err in statistics:
                            inp_er_l.append(int(inp_err.text))

                        tot_in_er = inp_er_l[0]

                    elif statistics.tag.find('output-error-list') != -1:
                        out_er_l = []

                        for out_err in statistics:
                            #print(out_err.text)
                            out_er_l.append(int(out_err.text))
                        tot_out_er = sum(out_er_l)

                    elif statistics.tag.find('queue-counters') != -1:
                        drop_list = []

                        for queue in statistics:
                            for drops in queue:
                                if drops.tag.find('queue-counters-total-drop-packets') != -1:
                                    drop_list.append(int(drops.text))
                        tot_drops = sum(drop_list)

                int_tup = (tot_out_er, tot_in_er, tot_drops)


                if int_dic.get(int_name, 0) == 0:
                    int_dic[int_name] = []
                if tot_drops != None:
                    int_dic[int_name].append(int_tup)
                if tot_drops == None:
                    int_bad[int_name] = 0

    for i in int_bad.keys():
        if i in int_dic:
            int_dic.pop(i)

    #print(int_dic)
    #print(int_bad.keys())
    delta_dic = {}
    for i in int_dic:
        try:
            delta_out_err = int_dic[i][rpc_num - 1][0] - int_dic[i][0][0]
            delta_in_err = int_dic[i][rpc_num - 1][1] - int_dic[i][0][1]
            delta_tot_drops = int_dic[i][rpc_num - 1][2] - int_dic[i][0][2]
        except:
            continue
        if (delta_in_err and delta_in_err > 1) or (delta_tot_drops and delta_tot_drops > 1):
            delta_dic[i] = (delta_in_err, delta_tot_drops)
    if delta_dic:
        for i in delta_dic:
            print("%s %s,%s,%s"% (fn, i, delta_dic[i][0], delta_dic[i][1]))
        #print("\n" + 50 * "#" + "\nDevice %s (inp err, total drops)\n" % fn + 50 * "#")
        #print(delta_dic)
###################################################################################################


###################################################################################################
def main():
    list_of_files = fn_l.fn_string.split('\n')
    print("Hostname,Input Errors,Interface Drops")
    for fn in list_of_files:
        rpc_reply_list, rpc_num = parse_file(fn)
        int_errors_delta(rpc_reply_list, rpc_num, fn)
###################################################################################################


if __name__ == "__main__":
    main()