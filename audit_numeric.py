#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)
#
# Only for use in auditing phase of data wrangling.
# For transformation to CSV & database, use "clean_address.py" instead

'''
Audit some numeric types in an OSM file
-- postal codes
      5-digit int
-- elevations
      OSM Wiki: default is meters, but local units of meas (feet in USA) is OK
-- height (variance in how expressed: int, float, meters, feet...)
      OSM Wiki: default is meters but can be int, float, or ' '' for feet-inch
      Incorrect values: no space between num and unit (eg 100m, not 100 m)
                        comma instead of decimal point
                        whitespace between ' and '' in feet-inches values
-- housenumbers
      does it start with a number? (the standard in US addresses)
'''

import xml.etree.cElementTree as ET
import re
from sys import argv

# REGULAR EXPRESSION PATTERNS
# This project used a location-specific data set based on Las Vegas NV USA.
# Las Vegas area postal code (5-digit or ZIP+4) patterns begin 890 or 891
postal_re = re.compile(r"(^89[01]\d\d$)|(^89[01]\d\d)(-\d\d\d\d$)")

# Housenumber starts with at least one digit, but no more than six
housenum_re = re.compile(r"^\d{1,6}")

# OSM-compliant "height" patterns:
#...................... digit(s), letter(s), sep by space
height_U_re = re.compile(r"^\d{1,5}\s[a-z]*$", re.IGNORECASE)
#...................... if "'" in value (ft' in")
height_Q_re = re.compile(r"^\d+\'\d\"|^\d+\'$")


# AUDITING FUNCTIONS

# Audit elevations
def check_NV_ele(n):
    '''Verify: if n is entirely numeric & no more than 5 digits, 
    it can be a valid US elevation. Also validate Nevada elevations.
    (https://wiki.openstreetmap.org/wiki/Key:ele)
    '''
    try:
        ele = float(n)
    except ValueError:
        return False
    if ele < 13500.0:  # No elevation in NV above this (src: USGS; Wikipedia)
        return True


# Audit heights
def check_height(n):
    '''Checks whether a number n conforms to correct format per OSM
       (https://wiki.openstreetmap.org/wiki/Key:height)
    '''
    if ',' in n:
        return False
    
    if (height_U_re.match(n) is not None) or (height_Q_re.match(n) is not None):
        return True
    
    try:
        # Check for both valid float & int values (ints can be cast as float)
        float(n)
        return True
    except ValueError:
        return False
    
    
# Audit postal codes
def check_ZIP(n):
    '''If n is 5 digits, or 5 digits-dash-4 digits, it can be a US postal code'''
    return (postal_re.match(n) is not None)


# Audit housenumbers
def check_housenum(n):
    '''Housenumber should begin with at least one digit'''
    return (housenum_re.match(n) is not None)


# Helper function for audit_num() function
def examine_problem(element, problems):
    '''find <tag/> attribute keys that failed audit; return a dict of them'''
    k = element.attrib['k']
    v = element.attrib['v']
    problems[k] = v
    return problems

# Run all audits
def audit_num(element, numerics, problems):
    '''If element is a <tag/>, audit its numeric attributes if present. 
       Return a dict (numerics) that tallies how many values failed audit.
    '''
    if element.tag == 'tag':
        k = element.attrib['k']
        v = element.attrib['v']
        
        # Map these 'k' attribs to specific audit functions for their 'v' values
        num_check = {'ele': check_NV_ele(v),
                     'height': check_height(v),
                     'addr:postcode': check_ZIP(v),
                     'tiger:zip_left': check_ZIP(v),
                     'addr:housenumber': check_housenum(v)}
        # Call audits for tags having attribs in the mapping
        if k in num_check.keys():
            # If a value failed audit, add it to its attrib's list of problems
            if num_check[k] == False:
                problems = examine_problem(element, problems)
                numerics[k] += 1
    
    return numerics
    

# MAP PROCESSING
def process_audits(osmfile):
    '''Parse an .osm file for auditing'''
    # Counts of the numeric tags that are to be audited
    numerics = {'ele': 0, 'height': 0, 'tiger:zip_left': 0, 'addr:postcode': 0, \
                'addr:housenumber': 0}
    # For the tags being audited, list any problematic values 
    problems = {'ele': [], 'height': [], 'addr:postcode': [], \
                'addr:housenumber':[]}
    
    for _, element in ET.iterparse(osmfile):
        numerics = audit_num(element, numerics, problems)

    return (numerics, problems)


if __name__ == '__main__':
    script, osmfile = argv
    a = process_audits(argv[1])
    print(a)