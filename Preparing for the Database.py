__author__ = 'thomaswoodside'
import xml.etree.cElementTree as ET
import re
import codecs
import json
import Improving_Street_Names

"""
Converts the XML Data into JSON-like data so that it can be loaded into MongoDB.
"""
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element, change_street_name_dict):
    node = {'created' : {}, 'pos' : []}
    if element.tag == "node" or element.tag == "way":
        node['type'] = element.tag
        if element.tag == 'way':
            for row in element:
                for a in row.attrib:
                    if a == 'ref':
                        try:
                            node['node_refs'].append(row.attrib[a])
                        except:
                            node['node_refs'] = []
                            node['node_refs'].append(row.attrib[a])
        for row in element.attrib:
            if row in CREATED:
                node['created'][row] = element.attrib[row]
                continue
            if row == 'lon':
                node['pos'] = node['pos'] + [float(element.attrib[row])]
                continue
            if row == 'lat':
                node['pos'] = [float(element.attrib[row])] + node['pos']
            else:
                node[row] = element.attrib[row]
        problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
        address = re.compile(r'addr:.')
        colon = re.compile(r'.:.')
        issue = False
        key = ''
        for row in element:
            for attribute in row.attrib:
                if attribute == 'k':
                    if problemchars.match(row.attrib[attribute]):
                        issue = True
                        continue
                    if address.match(row.attrib[attribute]):
                        if colon.findall(row.attrib[attribute][5:]): #checks to see if there are any other colons after 'addr:'
                            issue = True
                            continue
                        else:
                            address_key = row.attrib[attribute][5:]
                            key = ''
                    else:
                        key = row.attrib[attribute]
                        address_key = ''
                if attribute == 'v':
                    if issue:
                        issue = False
                        continue
                    if address_key != '':
                        if row.attrib[attribute] in change_street_name_dict: #this will clean the address keys in the method specified
                            try:
                                node['address'][address_key] = change_street_name_dict[row.attrib[attribute]]
                            except:
                                node['address'] = {}
                                node['address'][address_key] = change_street_name_dict[row.attrib[attribute]]
                        else:
                            try:
                                node['address'][address_key] = row.attrib[attribute]
                            except:
                                node['address'] = {}
                                node['address'][address_key] = row.attrib[attribute]
                        continue
                    if key != '':
                        node[key] = row.attrib[attribute]
                        continue
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    change_street_name_dict = Improving_Street_Names.modify_names() #provides the mapping to change street names
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element, change_street_name_dict)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

process_map("map")