#! /usr/bin/env python

try:
    from lxml import etree
except ImportError:
    print('Failed to import ElementTree from any known place')
    exit()
import re


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
def parse_xml_tree(rpc_reply_list, fn):
    # Iterrate over all XML trees
    # We have 2 XML trees in this example
    for xml_tree in rpc_reply_list:
        # Now we want to iterate over Elements inside "<route-engine>" element
        # Here we have 2 "<route-engine>" elements in each tree, that is why we need "for"
        for re in xml_tree.xpath("//*[local-name() = 'route-engine']"):
            # Each "re" is a list, because it contains more than one element, like slot,mastership-state,chassis-module
            for attribute in re:
                if attribute.tag.find('slot') != -1:
                    print("Printing all <slot>...</slot> elements: text:%s, tag:%s" % (attribute.text, attribute.tag))
                    '''
                    Result:
                    Printing all <slot>...</slot> elements: text:0, tag:slot
                    Printing all <slot>...</slot> elements: text:1, tag:slot
                    Printing all <slot>...</slot> elements: text:0, tag:slot
                    Printing all <slot>...</slot> elements: text:1, tag:slot
                    '''


            # Since it's a list we may use [] operator if we are shure in the position
            print("Printing all <mastership-state>...</mastership-state> elements: text:%s, tag:%s" % (re[1].text, re[1].tag))
            '''
            Result:
            Printing all <mastership-state>...</mastership-state> elements: text:master, tag:mastership-state
            Printing all <mastership-state>...</mastership-state> elements: text:backup, tag:mastership-state
            Printing all <mastership-state>...</mastership-state> elements: text:master, tag:mastership-state
            Printing all <mastership-state>...</mastership-state> elements: text:backup, tag:mastership-state
            '''

        # Or like this, from the main tree:
        print("Printing all <model-number>...</model-number> elements: text:%s, tag:%s" % (xml_tree[0][0][2][0].text, xml_tree[0][0][2][0].tag))
        '''
        Result:
        Printing all <model-number>...</model-number> elements: text:RE-S-1800X4-16G-S, tag:model-number
        Printing all <model-number>...</model-number> elements: text:RE1300, tag:model-number
        '''
        # <route-engine-information> - 0th element in <rpc_reply>
        # <route-engine> - 0th element in <route-engine-information>
        # <chassis-module> -3rd element in <route-engine>
        # <model-number> - 0th element in <chassis-module>
        #!!! But here we have 2 elements <route-engine> in each tree - we examined only first one.

        # Another example
        # Here we are going over "<chassis-module>" which contains only one element: <model-number>, but it still a list
        for model_num in xml_tree.xpath("//*[local-name() = 'chassis-module']"):
            print("Printing all <model-number>...<model-number> elements: text:%s, tag:%s" % (model_num[0].text, model_num[0].tag))
            '''
            Result:
            Printing all <model-number>...<model-number> elements: text:RE-S-1800X4-16G-S, tag:model-number
            Printing all <model-number>...<model-number> elements: text:RE-S-1800X4-16G-S, tag:model-number
            Printing all <model-number>...<model-number> elements: text:RE1300, tag:model-number
            Printing all <model-number>...<model-number> elements: text:RE1300, tag:model-number
            '''
            
            # Also getparent() is a very handy method
            
            print("Printing all <slot>...</slot> elements with **getparent** from <chassis-module>: text:%s, tag:%s" % (model_num.getparent()[0].text, model_num.getparent()[0].tag))
            '''
            Result:
            Printing all <slot>...</slot> elements with **getparent** from <chassis-module>: text:0, tag:slot
            Printing all <slot>...</slot> elements with **getparent** from <chassis-module>: text:1, tag:slot
            Printing all <slot>...</slot> elements with **getparent** from <chassis-module>: text:0, tag:slot
            Printing all <slot>...</slot> elements with **getparent** from <chassis-module>: text:1, tag:slot
            '''

###################################################################################################
def main():
    fn = 'sh_re_XML.txt'
    rpc_reply_list = parse_file(fn)
    parse_xml_tree(rpc_reply_list, fn)
###################################################################################################


if __name__ == "__main__":
    main()