import csv
import codecs
import re
import xml.etree.cElementTree as ET





osm_file = "bothell.osm"



lower_col = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problem_characters = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

nodes_csv = "nodes.csv"
nodes_tags_csv = "nodes_tags.csv"
ways_csv = "ways.csv"
ways_nodes_csv = "ways_nodes.csv"
ways_tags_csv = "ways_tags.csv"


nodes_fields = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
nodes_tags_fields = ['id', 'key', 'value', 'type']
ways_fields = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
ways_tags_fields = ['id', 'key', 'value', 'type']
ways_nodes_fields = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=nodes_fields, way_attr_fields=ways_fields,
                  problem_chars=problem_characters, default_tag='regular'):
   
    #Clean nodes or ways element to a dictionary

    nodes_attribs = {}
    ways_attribs = {}
    ways_nodes = []
    tags = []  

    if element.tag == 'node':
        for attrib in element.attrib:
            if attrib in nodes_fields:
                nodes_attribs[attrib] = element.attrib[attrib]
        
        for child in element:
            node_tag = {}
            if lower_col.match(child.attrib['k']):
                node_tag['type'] = child.attrib['k'].split(':',1)[0]
                node_tag['key'] = child.attrib['k'].split(':',1)[1]
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v']
                tags.append(node_tag)
            elif problem_characters.match(child.attrib['k']):
                continue
            else:
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v']
                tags.append(node_tag)
        
        return {'node': nodes_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in ways_fields:
                ways_attribs[attrib] = element.attrib[attrib]
        
        position = 0
        for child in element:
            way_tag = {}
            way_node = {}
            
            if child.tag == 'tag':
                if lower_col.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':',1)[0]
                    way_tag['key'] = child.attrib['k'].split(':',1)[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                elif problem_characters.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                    
            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                ways_nodes.append(way_node)
        
        return {'way': ways_attribs, 'way_nodes': ways_nodes, 'way_tags': tags}


#Helping Funcitons:
    

def take_element(osm_file, tags=('node', 'way', 'relation')):
    
    #take element if it is the right type of tag

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, base = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            base.clear()





class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


#Main Function

def process_map(file_in, validate):
    
    #processes each XML element and writes to csv(s)

    with codecs.open(nodes_csv, 'w') as nodes_file, \
         codecs.open(nodes_tags_csv, 'w') as nodes_tags_file, \
         codecs.open(ways_csv, 'w') as ways_file, \
         codecs.open(ways_nodes_csv, 'w') as way_nodes_file, \
         codecs.open(ways_tags_csv, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, nodes_fields)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, nodes_tags_fields)
        ways_writer = UnicodeDictWriter(ways_file, ways_fields)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, ways_nodes_fields)
        way_tags_writer = UnicodeDictWriter(way_tags_file, ways_tags_fields)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        

        for element in take_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
               

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

if __name__ == '__main__':
    process_map(osm_file, validate=True)

