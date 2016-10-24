#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)
#
# Transform the top-level attributes of an OpenStreetMap (OSM) file's 
# node elements from OSM format to CSV format.


import xml.etree.cElementTree as ET
import csv


# OSM node fields for CSV
header = ['id', 'type', 'changeset', 'lat', 'lon', 'timestamp', 'uid', 
          'user', 'version']


# Data Transformation
def shape_element(element):
    '''Get the specified attribute values of element. Return values as a list'''
    i = element.get('id')
    t = element.tag
    changeset = element.get('changeset')
    version = element.get('version')
    timestamp = element.get('timestamp')
    uid = element.get('uid')
    user = element.get('user')
    lat = element.get('lat')
    lon = element.get('lon')
    attr = [i, t, changeset, lat, lon, timestamp, uid, user, version]
    attr_enc = [a.encode('utf-8') for a in attr]   # Prevent encoding errors
    return attr_enc


# Map Processing
def process_map(file_in, file_out):
    '''read data from an OSM file, write to CSV file'''
    with open(file_out, 'wb') as f:
        writer = csv.writer(f, delimiter='|')  # '|' is sqlite default separator
        writer.writerow(header)
        for _, element in ET.iterparse(file_in, events=('start',)):
            if element.tag == "node":
                node_vals = shape_element(element)
                writer.writerow(node_vals)


if __name__ == "__main__":
    file_in = 'las-vegas.osm'  # default file for this project; can be changed.
    file_out = "{0}_nodes.csv".format(file_in[:-4])
    process_map(file_in, file_out)