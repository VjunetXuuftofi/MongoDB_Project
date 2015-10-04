__author__ = 'thomaswoodside'
"""
This file reads street names and creates a dictionary that maps the uncleaned street name to the cleaned street name with an ending.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "map"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", 'Circle', 'Crescent', 'Expressway', 'Plaza', 'Pulgas', 'Real', 'Terrace',
            'Walk', 'Way', 'Row', 'South', 'North', 'East', 'West']

mapping = { "St": "Street",
            "St.": "Street",
            'Ave' : 'Avenue',
            'Rd.' : 'Road',
            'Ave.' : 'Avenue',
            'Blvd' : 'Boulevard',
            'Cres' : 'Crescent',
            'Ct.' : 'Court',
            'Dr' : 'Drive',
            'Ln' : 'Lane',
            'Plz' : 'Plaza',
            'Rd' : 'Road',
            'St' : 'Street',
            'avenue' : 'Avenue',
            'parkway':'Parkway',
            'st' : 'Street',
            'Dr.' : 'Drive'
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types


def update_name(name, mapping):
    if name == None:
        return None
    street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
    street_type = re.findall(street_type_re, name)
    if street_type[0] in mapping:
        pos = name.find(street_type[0])
        name = name[:pos]
        name += mapping[street_type[0]]
        return name
    else:
        return name


def modify_names():
    st_types = dict(audit("map"))
    dictionary = {}
    for ways in st_types:
        for name in st_types[ways]:
            better_name = update_name(name, mapping)
            dictionary[name] = better_name
    return dictionary

if __name__ == '__main__':
    print(modify_names())