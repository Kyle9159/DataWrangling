#Counts multiple patterns in the tags

import xml.etree.cElementTree as ET
from collections import defaultdict

#Returns a dictionary of top level tags and their counts
def count_tags(filename):
        tags_dict = defaultdict(int)
        for event, elem in ET.iterparse(filename):
            tags_dict[elem.tag] += 1
        return tags_dict