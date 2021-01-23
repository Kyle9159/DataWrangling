import csv 
import sqlite3


#Creating the database file
db_file = 'bothell.db'

#Connecting to the database
conn = sqlite3.connect(db_file)
conn.text_factory = str

#Curser
cur = conn.cursor()



#Drop the nodes_tags table if it already exists

cur.execute(''' DROP TABLE IF EXISTS nodes_tags''')
conn.commit()

#Creating the table nodes_tags
cur.execute('''
	CREATE TABLE nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
)''')

conn.commit()


cur.execute(''' DROP TABLE IF EXISTS nodes''')
conn.commit()
#Creating the table nodes
cur.execute('''
	CREATE TABLE nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
)''')

conn.commit()

#Drop the ways table if it already exists
cur.execute(''' DROP TABLE IF EXISTS ways''')
conn.commit()

#Creating the table ways
cur.execute('''
CREATE TABLE ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
)''')

conn.commit()

#Drop the ways_tags table if it already exists
cur.execute(''' DROP TABLE IF EXISTS ways_tags''')
conn.commit()

#Creating the table ways_tags
cur.execute('''
CREATE TABLE ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
)''')

conn.commit()

#Drop the ways_nodes table if it already exists
cur.execute(''' DROP TABLE IF EXISTS ways_nodes''')
conn.commit()

#Creating the table ways_nodes
cur.execute('''
CREATE TABLE ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
)''')

conn.commit()



#Reading the csv file as a dictionary and formatting the data as a list of tubles:

with open('nodes_tags.csv', 'r') as fin:
	dr = csv.DictReader(fin) 
	to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

#inserting the formatted data

cur.executemany('INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);', to_db)

conn.commit()

#Continuing with the other csv files:
with open('ways_tags.csv', 'r') as fin:
	dr = csv.DictReader(fin) 
	to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

cur.executemany('INSERT INTO ways_tags(id, key, value,type) VALUES (?, ?, ?, ?);', to_db)

conn.commit()


with open('nodes.csv', 'r') as fin:
	dr = csv.DictReader(fin)
	to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'] ) for i in dr]

cur.executemany('INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);', to_db)

conn.commit()


with open('ways.csv', 'r') as fin:
	dr = csv.DictReader(fin) 
	to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'] ) for i in dr]

cur.executemany('INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);', to_db)
# commit the changes
conn.commit()


with open('ways_nodes.csv', 'r') as fin:
	dr = csv.DictReader(fin) 
	to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

cur.executemany('INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);', to_db)

conn.commit()



#Closing connection

conn.close()
