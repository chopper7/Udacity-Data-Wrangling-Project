#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Based on: "Udacity Data Wrangling, PS 6-5: Preparing for Database"
# Coded for Python 2.7 (as used in Udacity course)
#
# Reads an OSM map file, cleans its node elements' attribute values,
# then writes a subset of them to a CSV file for importation into a database.


import csv
import xml.etree.cElementTree as ET
import clean_address  # street name cleaning script
import clean_chars    # problem characters script
#from sys import argv  ## Uncomment this line if using non-default args


# Specific "k"s to extract from <tag/>s for use as fieldnames
k_keys = ['aeroway', 'amenity', 'barrier', 'building', 'created_by', 'cuisine',
          'ele', 'FIXME', 'highway', 'import_uuid', 'landuse', 'leisure',
          'name', 'natural', 'parking', 'place', 'power', 'railway', 'ref',
          'religion', 'review', 'shop', 'source', 'source_ref', 'tourism',
          'waterway', 'gnis:ST_alpha', 'gnis:county_name', 'gnis:County',
          'gnis:Class', 'gnis:feature_type','gnis:feature_id', 'gnis:county_id',
          'gnis:state_id', 'gnis:id', 'gnis:ST_num', 'gnis:created',
          'gnis:County_num','gnis:edited','gnis:name']

# Fields (columns) that will be in CSV header and the database
# (includes attributes that are specific to node-elements, not in way-elements)
fields = ['node_id', 'type', 'address', 'addr_city', 'addr_housename',
          'addr_housenumber', 'addr_postcode', 'addr_state', 'addr_street',
          'aeroway', 'amenity', 'barrier', 'building',  'created_by', 'cuisine',
          'ele', 'FIXME', 'gnis_Class', 'gnis_County', 'gnis_County_num',
          'gnis_county_id','gnis_county_name', 'gnis_created', 'gnis_edited',
          'gnis_feature_id', 'gnis_feature_type', 'gnis_id', 'gnis_name',
          'gnis_ST_alpha', 'gnis_ST_num', 'gnis_state_id', 'highway',
          'import_uuid', 'landuse', 'leisure','name', 'natural', 'parking',
          'place', 'power', 'railway', 'ref', 'religion', 'review', 'shop',
          'source', 'source_ref', 'tourism', 'waterway']


def shape_element(element):
    '''shape an OSM "node" element's tag attributes into csv-compatible dict'''
    # Initialize a dict to hold tag data
    # (populate as null any fields that have no k:v data to fill in)
    tag_attrs = dict().fromkeys(fields, None)
    
    # Set the first two fields (present in every element)
    tag_attrs['node_id'] = element.get('id')
    tag_attrs['type'] = element.tag

    for tag in element.iter('tag'):
        k = tag.attrib['k']
        v = clean_chars.process_values(tag, enc=True)  # clean characters in v
        
        # Clean address values, then map to fields
        if k.startswith('addr:'):
            # flag node as having "addr" (to use in combined queries)
            tag_attrs['address'] = 'addressed'
            # clean the values
            k = k.replace(':', '_')
            if k == 'addr_state':
                v = clean_address.clean_state(v)
            elif k == 'addr_postcode':
                v = clean_address.clean_postal(v)
            else:
                v = clean_address.clean_streetname(v)
                v = clean_address.clean_nsew(v)
            # set the key to cleaned value
            if k in fields:
                tag_attrs[k] = v
                
        # Clean other attribute values, then map to fields
        if k in k_keys:
            k = k.replace(':', '_')
            if k == 'name':
                v = clean_address.clean_streetname(v)
                v = clean_address.clean_nsew(v)
            # set the key to cleaned value
            tag_attrs[k] = v

    return tag_attrs


# MAP PROCESSING

# Initialize a list of dicts of node element ids and their child tag attributes
nodes = []

def process_map(file_in, file_out):
    '''Parse an OSM map file (file_in), 
       clean/transform its node element attribute values,
       then write them to a CSV file (file_out).
       Note, "|" is SQLite3's default delimiter
    '''
    with open(file_out, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        writer.writeheader()
        for _, element in ET.iterparse(file_in, events=('start',)):
            if element.tag == 'node':
                nodes.append(shape_element(element))
        writer.writerows(nodes)


if __name__ == "__main__":
    # Uncomment the next line to use with other OSM map files    
    #script, file_in = argv
    
    # Default file for project; comment-out this line to use a different map
    file_in = 'las-vegas.osm'
    file_out = "{0}_node_tags.csv".format(file_in[:-4])
    process_map(file_in, file_out)
