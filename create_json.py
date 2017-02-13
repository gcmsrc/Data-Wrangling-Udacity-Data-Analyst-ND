# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 12:03:07 2016

@author: gsarchioni
"""

"""
    This file contains the single function used to created a cleansed and formatted
    .json file for an .osm file.

    Module-level variables are:

        node_types (list): list of node types to be added to the .json file.


"""


import xml.etree.ElementTree as ET
import codecs
import json
import element

node_types = ['way','node','relation']



def process_map(file_in, file_out, pretty = False):

    """
        This function is used create a .json file formatted according to the specifics
        defined in the element module

        Argument:
            file_in (string): name of the .osx xml file. It must be stored in the same folder
                              of this code (otherwise it is necessary to specify path through
                              os module).
            file_out (string): name of the output file
            pretty (bool): keyworkd parameter to choose pretty printing of the .json file. Please
                           note that if True, file cannot be uploaded into MongoDB.

        Returns:
            json_file: .json file.
    """
    
    file_out = "{0}.json".format(file_out)
    json_file = []
    with codecs.open(file_out, "w") as fo:
        for _, item in ET.iterparse(file_in):
            if item.tag in node_types:
                el = element.shape_element(item)
                if el:
                    json_file.append(el)
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
    return json_file


   
process_map('milan.osm','milan2')