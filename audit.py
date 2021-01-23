import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = "bothell.osm"

street_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected_types = [ "Alley", "Avenue", "Boulevard", "Center", "Circle", "Commons", 
            "Court", "Cove",  "Drive", "Highway", "Lane", "Mission", "Northeast", "Northwest" , "Parkway",   
            "Park", "Path", "Place", "Plaza",  "Road", "Southast", "Southwest" "Square", "Street", 
            "Trail","Walk", "Way",]


mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "avenue": "Avenue",
            "ave": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Blvd,": "Boulevard",
            "Boulavard": "Boulevard",
            "Boulvard": "Boulevard",
            "Ct": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "E": "East",
            "Hwy": "Highway",
            "Ln": "Lane",
            "Ln.": "Lane",
            "N": "North",
            "Pl": "Place",
            "Plz": "Plaza",
            "Rd": "Road",
            "Rd.": "Road",
            "S:": "South",
            "St": "Street",
            "St.": "Street",
            "st": "Street",
            "street": "Street",
            "square": "Square",
            "parkway": "Parkway",
            "W": "West",
            "NW": "Northwest",
            "NE": "Northeast",
            "SW": "Southwest",
            "sw": "Southwest",
            "SE": "Southeast",
            "state": "State",
            "99": "Highway 99",
            "WA-99":"Highway 99"
            }


def check_street_type(street_types, street_name):
    s = street_re.search(street_name)
    if s:
        street_type = s.group()
        if street_type not in expected_types:
            street_types[street_type].add(street_name)

            
def street_name(elem):
    return (elem.attrib['k'] == "addr:street")



def audit(osmfile):
    osm_file = open('bothell.osm', 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if street_name(tag):
                    check_street_type(street_types, tag.attrib['v'])
    return street_types



def fix_street(osmfile):
    st_types = audit(osmfile)
    for st_type, ways in st_types.iteritems():
        for name in ways:
            if st_type in mapping:
                better_name = name.replace(st_type, mapping[st_type])
                print (name, "=>", better_name)


### audit zip code

import pandas as pd                 
# zip code data from: http://www.unitedstateszipcodes.org/zip-code-database/
zipcode = pd.read_csv("zip_code_database.csv", error_bad_lines=False)
bothell_zipcode = zipcode[(zipcode.primary_city == "Bothell") & (zipcode.state == "WA")].zip
            
bothell_zipcode_str = [str(x) for x in list(bothell_zipcode)]



def audit_postcode(filename):
    osm_file = open(filename, "r")  
    code_list = set()
    long_code = 0
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "addr:postcode":
                    if len(tag.attrib['v']) > 5:
                        long_code += 1
                        tag.attrib['v'] = tag.attrib['v'].split('-')[0]
                    code_list.add(tag.attrib['v'])               
    print('There are '+ str(long_code) + ' long post codes.')
    return [code for code in code_list if code not in bothell_zipcode_str]      
