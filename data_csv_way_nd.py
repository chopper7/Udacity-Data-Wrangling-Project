#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)
#
# Transform the node numbers referred to in an OpenStreetMap
# (OSM) file's "way" elements to CSV format.

import xml.etree.cElementTree as ET
import csv

waynd = []  # list of dicts of way ids and their nd refs

fieldnames = ['way_id', 'node_refs']


# Data Transformation
def shape_element(element):
    '''From a <way> element, build and return a dict of way ids and nd refs'''
    wndrefs = {}
    w_id = element.get('id')                                # <way>'s unique id
    ndlist = [nd.get('ref') for nd in element.iter('nd')]   # gather all nd refs
    wndrefs['way_id'] = w_id
    wndrefs['node_refs'] = ' '.join(ndlist)     # concat refs to string for csv
    return wndrefs


# Map Processing
def process_map(file_in, file_out):
    '''
    file_in  -- name (str) of an OSM file containing XML data
    file_out -- name (str) of a CSV file, written from file-in's <way> nd refs
    '''
    with open(file_out, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames, delimiter='|')
        writer.writeheader()
        for _, element in ET.iterparse(file_in, events=('start',)):
            if element.tag == "way":
                waynd.append(shape_element(element))
        writer.writerows(waynd)


if __name__ == "__main__":
    file_in = 'las-vegas.osm'  # default file for this project; can be changed.
    file_out = "{0}_way_nd.csv".format(file_in[:-4])
    process_map(file_in, file_out)