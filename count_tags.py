#!/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the
tag name as the key and number of times this tag can be encountered in
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    dictionary = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in dictionary:
            dictionary[elem.tag] += 1
        else:
            dictionary[elem.tag] = 1
    return dictionary



def test():

    tags = count_tags('map')
    pprint.pprint(tags)



if __name__ == "__main__":
    test()