**How It works**

1) Creating XML trees.
The function ```"parse_file(filename)"``` takes a file and clears it out from crap and creates a new temporary file called ```'tmp.xml'```. This file can be viewed in the directory.

Then it opens this temp file and makes XML trees (yes, file may contain multiple XML outputs) with root ```"<rpc-reply>"``` and returns the list of these trees (list_of_xml_trees).

```
rpc_reply_list = parse_file(fn)
print rpc_reply_list

#returns#

[<Element rpc-reply at 0x10e634518>, <Element rpc-reply at 0x10e634488>]
```

File contained 2 XML outputs, so we got the list with 2 XML trees (elements) with root elements "<rpc-reply>".

2) Parsing XML trees.

These trees are like lists of special elements. We can iterate through the trees.
Each element has 2 parameters: tag and text

```<model-number>RE-S-1800X4-16G-S</model-number>```

tag == 'model-number'
text == 'RE-S-1800X4-16G-S'

Example:
```
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
```
