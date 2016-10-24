#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)

'''
Cleaning & standardizing address values in OpenStreetMap data
  -- problem characters (e.g., "Street\\")
  -- abbreviations
  -- inconsistencies

This is a helper script with functions that can be imported into and
used in other, data-to-csv transformation scripts.
'''

#import xml.etree.cElementTree as ET
import re
from sys import argv

# REGEX patterns to search for
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)  # find last word
nsew_re = re.compile(r'N |N\. |S |S\. |E |E\. |W |W\. ')  # find compass letter
postal_re = re.compile(r'(\d{5})')  # find postal code

# mapping of states to abbreviations -- Nevada and bordering states
states = {'Arizona': 'AZ',
          'California': 'CA',
          'Nevada': 'NV',
          'Utah': 'UT'}

# mapping of directional abbreviations to full words
nsew_unabbrev = {'N ': 'North ', 'N. ': 'North ',
                 'S ': 'South ', 'S. ': 'South ',
                 'E ': 'East ', 'E. ': 'East ',
                 'W ': 'West ', 'W. ': 'West '}

# mapping of street type abbreviations to full words
street_unabbrev = \
{'Ave': 'Avenue', 'AVE': 'Avenue', 'Ave.': 'Avenue',
 'Blvd': 'Boulevard', 'Blvd.': 'Boulevard',
 'Cir': 'Circle', 'Cir.': 'Circle',
 'Crt': 'Court', 'Crt.': 'Court',
 'Ct': 'Court', 'Ct.': 'Court',
 'Dr': 'Drive', 'Dr.': 'Drive',
 'E.': 'East',
 'Fwy': 'Freeway', 'Fwy.': 'Freeway',
 'Hwy': 'Highway', 'Hwy.': 'Highway',
 'Ln': 'Lane', 'Ln.': 'Lane',
 'Mt': 'Mountain', 'Mt.': 'Mountain',
 'N.': 'North',
 'Pkwy': 'Parkway', 'Pkwy.': 'Parkway',
 'Pl': 'Place', 'Pl.': 'Place',
 'Pt': 'Point', 'Pt.': 'Point',
 'Rd': 'Road', 'Rd.': 'Road',
 'Rte': 'Route', 'Rte.': 'Route',
 'S.': 'South',
 'Sq': 'Square', 'Sq.': 'Square',
 'St': 'Street', 'St.': 'Street',
 'Ter': 'Terrace', 'Ter.': 'Terrace',
 'Tr': 'Trail', 'Tr.': 'Trail',
 'W.': 'West',
 'Wy': 'Way', 'Wy.': 'Way'}


# CLEANING FUNCTIONS

def clean_streetname(name):
    '''In name, replace abbreviated street types with full words'''
    m = street_type_re.search(name)
    if m and  m.group() in street_unabbrev:
        name = name.replace(m.group(), street_unabbrev[m.group()])
    # Munge the Las Vegas "Strip" because street-type not at end of string
    if 'Vegas Blvd' in name:
        name = name.replace('Blvd', 'Boulevard')
    return name


def clean_nsew(name):
    '''In name, replace abbreviated compass words with full words'''
    m = nsew_re.search(name)
    if m:
        name = name.replace(m.group(), nsew_unabbrev[m.group()])
    return name


def clean_state(value):
    '''Ensure state value is a 2-character abbreviation'''
    if len(value) != 2 and value in states:    
        value = states.get(value)
    return value

    
def clean_postal(value):
    '''Search for 5 consecutive digits in string value; 
       if found, return the digits as a string.
       Or else, return original input string.
    '''
    m = postal_re.search(value)
    if m:
        value = m.group()
    return value


def is_addr_street(tag):
    '''T|F: does an osm tag specify a street address?'''
    return (tag.attrib['k'] == 'addr:street')


# MAP PROCESSING

def process_tag(element):
    '''element is a <node> or a <way>'''
    for tag in element.iter("tag"):
        value = clean_streetname(tag.attrib['v'])
        value = clean_nsew(tag.attrib['v'])
        return value


if __name__ == "__main__":
    script, element = argv
    #for _, element in ET.iterparse(osmfile):  ## Uncomment if standalone script
    if element.tag == "tag":
        s = process_tag(element)
        print(s)
