#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Based on: "Udacity Data Wrangling, PS 6-3: Exploring Users", `users.py`
# Coded for Python 2.7 (as used in Udacity course)
#
# Enumerate and\or audit user names from an OpenStreetMap XML file.


import xml.etree.cElementTree as ET
import re
from sys import argv


# REGEX pattern -- Problematic characters pattern
problemchars = re.compile(r"[=\+/&<>:;\''\?%#$@\,\.\t\r\n]")
# REGEX pattern --  HTML character entity pattern ("&nbsp;" , "&#160;")
html_ents = re.compile(r"(&[a-z]+;)|(&#\d+;)")

# Capture any user names found by character audit
problem_usernames = set()  


def audit_users(users):
    '''Check if user name is missing, is an empty string,
       has problem characters, or has HTML character entities.
    '''
    audit_tally = {'no attribute': 0, 'empty': 0, 'problem character': 0, \
                  'html char entity': 0, 'okay': 0}
    
    for user in users:
        if user is None:
            audit_tally['no attribute'] += 1
        elif user == '':
            audit_tally['empty'] += 1
        elif re.search(problemchars, user):
            audit_tally['problem character'] += 1
            problem_usernames.add(user)  # capture that user name
        elif re.search(html_ents, user):
            audit_tally['html char entity'] += 1
            problem_usernames.add(user)  # capture that user name
        else:
            audit_tally['okay'] += 1

    return audit_tally, problem_usernames


# MAP PROCESSING

def process_map(osmfile, audit=True):
    '''Collect usernames from osmfile.
      If audit=True (default), run `audit_users` function to check for missing
             entries or potential problem characters. Return the audit results.
      If audit=False, just Return a set of user names.
    '''
    users = set()  # Many users have multiple entries - only need each once
    
    for _, element in ET.iterparse(osmfile, events=('start',)):
        if element.tag in ('node', 'way', 'relation'):        
            users.add(element.get('user'))
            
    if audit:
        results = audit_users(users)  # Audit the user name values
        print(results)
    else:
        results = users               # or just return a set of names
        print("{} unique users in data set.".format(str(len(users))))
        
    return results


if __name__ == "__main__":
    script, osmfile = argv  # argv[0], argv[1] = argv
    process_map(argv[1])
