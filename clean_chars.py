#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, Problem Set 6"
# Coded for Python 2.7 (as used in Udacity course)

'''
For use with OpenStreetMap data.
Replace potentially problematic characters with ones that won't crash the
transformation of OSM data into CSV files.

For example:
  Replace commas with spaces so as not to interfere with CSV.
  Replace double-quotes, such as in <a href=", with empty strings.
  
Script could be a standalone and receive an osmfile, or be imported into 
another script to clean OSM tags individually.
'''

import xml.etree.cElementTree as ET
import re
from sys import argv

# Auditing showed the following characters to be problematic when transforming
# data:  commas, double-quotes, tabs, returns and newline characters
# REGEX for problematic characters
problem_chars = re.compile(r'[\,"\t\r\n]')  


def clean_problems(s):
    '''For string `s`, replace problem character patterns with empty string.
       Return new "cleaned" string.
    '''
    newval = s
    rpl = re.sub(problem_chars, '' , s)  # set the replacement string
    if rpl != s:      # If it looks like s has been altered:
        newval = rpl  # assign newval to rpl.
    return newval


def has_problem(s):
    '''For string `s`, search for problematic character pattern matches.
       Return True|False.
    '''
    m = re.search(problem_chars, s)  # Either a Match or None
    return (m is not None)


# MAP PROCESSING
def process_values(tag, enc=False):
    '''If a tag's "v" value has problems, return a cleaned-up value;
       otherwise just return the original "v" value.
       Set enc=True if Encoding Errors are being thrown.
    '''
    if enc:
        val = tag.attrib['v'].encode('utf-8')  # Prevent encoding errors
    else:
        val = tag.attrib['v']
    if has_problem(val):           # If val has problem characters:
        val = clean_problems(val)  # send val to get cleaned
    return val


if __name__ == "__main__":
    script, osmfile = argv  # argv[0], argv[1] = argv
    for _, element in ET.iterparse(osmfile):
        if element.tag == "node" or element.tag == "way":
            for tag in element.iter("tag"):
                k = tag.attrib['k']
                v = process_values(tag)
