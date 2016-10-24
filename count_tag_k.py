#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Writes a plain text file listing all the distinct "k" tag attribute
values in an OpenStreetMap element, sorted by most to fewest.

in_file: OpenStreetMap file in .osm (xml) format
out_file: plain text file for writing output of "k" list
elem_type: an OSM element (way, node, etc.)
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
from sys import argv

script, in_file, out_file, elem_type = argv

# Example arguments
#infile = 'las-vegas.osm'
#outfile = 'way_tags.txt'
#elem_type = 'way'

tags = defaultdict(int)

# Find, parse, and count the tag "k" attributes of specified element
for _, element in ET.iterparse(in_file):
    if element.tag == elem_type:
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            #v = tag.attrib['v']  # uncomment to enumerate "v"s too
            tags[k] += 1

# Write to file the "k" attributes, sorted by count descending
with open(out_file, 'w') as f:
    for k, cnt in sorted(tags.items(), key=lambda (k,cnt): cnt, reverse=True):
        f.write(k + ': ' + str(cnt) + '\n')

