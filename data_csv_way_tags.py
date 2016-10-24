#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on "Udacity Data Wrangling, PS 6-5: Preparing for Database"
# Coded for Python 2.7 (as used in Udacity course)
#
# Reads an OSM map file, cleans its way elements' attribute values,
# then writes a subset of them to a CSV file for importation into a database.


import csv
import xml.etree.cElementTree as ET
import clean_address  # street name cleaning script
import clean_chars    # problem characters script

# Specific "k"s to extract from <tag/>s for use as fieldnames
k_keys = ['access', 'aeroway', 'amenity', 'barrier', 'bicycle', 'bridge',
         'building', 'building:levels', 'created_by', 'cuisine', 'ele', 'FIXME',
         'foot', 'footway', 'gnis:county_id', 'gnis:county_name', 'gnis:created',
         'gnis:edited', 'gnis:fcode', 'gnis:feature_id', 'gnis:feature_type',
         'gnis:ftype', 'gnis:id', 'gnis:state_id', 'golf', 'hgv', 'highway',
         'landuse', 'lanes', 'leisure', 'name', 'name_1', 'natural', 'oneway',
         'parking', 'place', 'power', 'railway', 'ref', 'religion', 'review',
         'service', 'shop', 'source', 'source_ref', 'sport', 'surface',
         'tourism', 'water', 'waterway']

# Fields (columns) that will be in CSV header and the database
# (includes attributes that are specific to way-elements, not in node-elements)
fields = ['way_id', 'type', 'address','addr_city','addr_county','addr_housename',
         'addr_housenumber', 'addr_postcode', 'addr_state', 'addr_street',
         'access', 'aeroway', 'amenity', 'barrier', 'bicycle', 'bridge',
         'building', 'building_levels', 'created_by', 'cuisine', 'ele', 'FIXME',
         'foot', 'footway', 'golf', 'hgv', 'highway', 'landuse', 'lanes',
         'leisure', 'name', 'name_1', 'natural', 'oneway', 'parking', 'place',
         'power', 'railway', 'ref', 'religion', 'review', 'service', 'shop',
         'source', 'source_ref', 'sport', 'surface', 'tourism', 'water',
         'waterway', 'gnis_county_id', 'gnis_county_name', 'gnis_created',
         'gnis_edited', 'gnis_fcode', 'gnis_feature_id', 'gnis_feature_type',
         'gnis_ftype', 'gnis_id', 'gnis_state_id', 'tiger_cfcc', 'tiger_county',
         'tiger_mtfcc', 'tiger_name_base', 'tiger_name_base_1',
         'tiger_name_direction_prefix', 'tiger_name_direction_prefix_1',
         'tiger_name_direction_suffix', 'tiger_name_direction_suffix_1',
         'tiger_name_full', 'tiger_name_type', 'tiger_name_type_1',
         'tiger_reviewed', 'tiger_separated', 'tiger_source', 'tiger_tlid',
         'tiger_upload_uuid', 'tiger_zip_left', 'tiger_zip_right']


# DATA TRANSFORMATION
def shape_element(element):
    '''shape an OSM "way" element's tag attributes into csv-compatible dict'''
    # Initialize a dict to hold tag data 
    # (populate as null any fields that have no k:v data to fill in)
    tag_attrs = dict().fromkeys(fields, None)
    
    # Set the first two fields (present in every element)
    tag_attrs['way_id'] = element.get('id')
    tag_attrs['type'] = element.tag
    
    # Get and clean any of this tag's k:v pairs that will go into the CSV file
    for tag in element.iter('tag'):
        k = tag.attrib['k']
        v = clean_chars.process_values(tag, enc=True)  # clean characters in v
        
        # Clean address values, then map to fields
        if k.startswith('addr:'):
            # flag way as having "addr" (to use in combined queries)
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
        
        # Clean TIGER attribute values, then map to fields
        if k.startswith('tiger:'):
            k = k.replace(':', '_')
            if k.endswith('full'):
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
            # set the prepped key and value
            tag_attrs[k] = v

    return tag_attrs


# MAP PROCESSING

# Initialize a list of dicts of way element ids and their child tag attributes
ways = []

def process_map(file_in, file_out):
    '''Parse an OSM map file (file_in), 
       clean/transform its way element attribute values,
       then write them to a CSV file (file_out).
       Note, "|" is SQLite3's default delimiter
    '''
    with open(file_out, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='|')
        writer.writeheader()
        for _, element in ET.iterparse(file_in, events=('start',)):
            if element.tag == 'way':
                ways.append(shape_element(element))
        writer.writerows(ways)


if __name__ == "__main__":
    file_in = 'las-vegas.osm'  # default file for this project; can be changed.
    file_out = "{0}_way_tags.csv".format(file_in[:-4])
    process_map(file_in, file_out)
