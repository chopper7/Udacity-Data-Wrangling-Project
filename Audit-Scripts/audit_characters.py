#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Audit OSM file for potentially problematic characters.
# Only for use in auditing phase of data wrangling.
# For transformation to CSV & database, use "clean_character.py" instead.


import xml.etree.cElementTree as ET
import re
from sys import argv


# REGEX pattern -- Problematic characters pattern
problemchars = re.compile(r"[=\+<>\?%$@\,\t\r\n]") #(removed): \''
# REGEX pattern -- HTML character entity pattern -- e.g., "&nbsp;" or "&#160;"
html_ents = re.compile(r"(&[a-z]+;)|(&#\d+;)")

# Collection for capturing user names that "fail"audit
problem_values = set()


def auditor(value):
    '''check value for empty strings and problematic characters'''
    value_audit = {'empty': 0, 'problem character': 0, 'html char entity': 0} #, 'okay': 0}

    if value == '':
        value_audit['empty'] += 1
        
    if re.search(problemchars, value):
        value_audit['problem character'] += 1
        problem_values.add(value)  # capture that value
        
    if re.search(html_ents, value):
        value_audit['html char entity'] += 1
        problem_values.add(value)  # capture that value
        
    #value_audit['okay'] += 1  ## uncomment if counting "okay" characters
    return value_audit, problem_values


# MAP PROCESSING
def process_map(osmfile, audit=True):
    for _, element in ET.iterparse(osmfile, events=('start',)):
        if element != 'tag':
            # send element's attribute values to auditing function
            for key in element.attrib:
                results = auditor(element.get(key))
        else:   
            # element is <tag/>, so send v's value to auditing function
            results = auditor(element.attrib['v'])
    return results


if __name__ == "__main__":
    script, osmfile = argv  # argv[0], argv[1] = argv
    process_map(argv[1])
