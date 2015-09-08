__author__ = 'thomaswoodside'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

import Improving_Street_Names

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
                        if row.attrib[attribute] in change_street_name_dict: #this will make sure that the street names are edited properly
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