#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Audit OSM address data for street types
# Only for use in auditing phase of data wrangling.
# For transformation to CSV & database, use "clean_address.py" instead

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

# REGEX:last word in string
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Typical, common street name suffixes
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", \
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]

mapping = { "St": "Street", "St.": "Street", "Ave": "Avenue", "Rd.": "Road" }


def street_endings(streets, street_name):
    '''collects ALL last-words from "street" values'''
    m = street_type_re.search(street_name)   # grab last word in a street name
    if m:
        streets[m.group()].add(street_name)
    return streets


def audit_street_type(street_types, street_name):
    '''search for unexpected streettype names and add to `street_types` dict'''
    m = street_type_re.search(street_name)   # grab last word in a street name
    if m:                                    # m as in "match"
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_addr_street(tag):
    '''T|F: does an osm tag specify a street address?'''
    return (elem.attrib['k'] == 'addr:street')


def audit_streets(osmfile, include_names=False):
    '''copy of audit(), adapted for street_endings function'''
    # Initialize a "street-type" collection:
    # `defaultdict` avoids duplicate keys, and `set` collects unique names
    #  of streets for each particular street_types key's value.
    streets = defaultdict(set)
    
    # Parse nodes and ways for tags with street in them, then audit
    for event, elem in ET.iterparse(osmfile, events=('start',)):
        if elem.tag == 'node'or elem.tag == 'way':
            for tag in elem.iter("tag"):
                if tag.get('k') == 'name':
                    name = tag.get('v')  # hold the name in case we need it
                if is_addr_street(tag):  # If it has a street name attrib
                    street_endings(streets, name)
    if include_names == True:
        results = streets.copy()          # unique keys & all values for each
    else:
        results = sorted(streets.keys())  # only unique keys, not their values
    return results


def tag_in_node(osmfile, e, a):
    '''e: element ('node', 'way', etc.)
       a: substring or value of a "k" ('addr', 'tiger', etc.)
       Return collection of a's in an e, if any
    '''
    streets = defaultdict(list)
    count = 0
    for event, elem in ET.iterparse(osmfile, events=("start",)):
        if elem.tag == e:
            for tag in elem.iter("tag"):
                if a in tag.attrib['k']:
                    count += 1
                    streets[tag.attrib['k']] = tag.attrib['v']
    return streets


def audit(osm_file):
    '''auditing a file for street names having "unexpected" street suffixes
       return a dict called `street_types` (see below)
       Not run automatially, call just when auditing.
    '''
    osm_file = open(osm_file, "r")
    # Initialize a "street-type" collection:
    # `defaultdict` avoids duplicate keys, and `set` collects unique names
    #  of streets for each particular street_types key's value.
    street_types = defaultdict(set)
    # Parse nodes and ways for tags with street in them, then audit
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):      # <tag/>s in 'node' or 'way' elems
                if has_street_name(tag):      
                    audit_street_type(street_types, tag.attrib['v']) # audit it
    osm_file.close()
    return street_types


def update_name(name, mapping):
    '''Cleaning: get unexpected part of name; replace with 'expected' name
       Not run automatially, call just when auditing.
    '''
    suffix = street_type_re.search(name).group(0)
    name = name.replace(suffix, mapping[suffix])
    return name


# MAP PROCESSING
def process_map(osmfile):
    street_endings = audit_streets(osmfile)


if __name__ == '__main__':
    script, osmfile = argv
    process_map(argv[1])
