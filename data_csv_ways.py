#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)

'''
Transform the top-level attributes of an OpenStreetMap (OSM) file's 
way elements from OSM format to CSV format.
'''

import xml.etree.cElementTree as ET
import csv

# OSM way fields for CSV
header = ['id', 'type', 'changeset', 'timestamp', 'uid', 'user', 'version']


# DATA TRANSFORMATION
def shape_element(element):
    '''Get the specified attribute values of element. Return values as a list'''
    i = element.get('id')
    t = element.tag
    changeset = element.get('changeset')
    version = element.get('version')
    timestamp = element.get('timestamp')
    uid = element.get('uid')
    user = element.get('user')
    attr = [i, t, changeset, timestamp, uid, user, version]
    attr_enc = [a.encode('utf-8') for a in attr]  # Prevent encoding errors
    return attr_enc


# MAP PROCESSING
def process_map(file_in, file_out):
    with open(file_out, 'wb') as f:
        writer = csv.writer(f, delimiter='|')  # '|' is sqlite default separator
        writer.writerow(header)
        for _, element in ET.iterparse(file_in, events=('start',)):
            if element.tag == "way":
                way_vals = shape_element(element)
                writer.writerow(way_vals)


if __name__ == "__main__":
    file_in = 'las-vegas.osm'  # default file for this project; can be changed.
    file_out = "{0}_ways.csv".format(file_in[:-4])
    process_map(file_in, file_out)
