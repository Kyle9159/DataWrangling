import sqlite3

#GitHub - ian-whitestone/data-wrangling-openstreetmap .... https://github.com/ian-whitestone/data-wrangling-openstreetmap

def num_nodes():
    result = cur.execute('SELECT COUNT(*) FROM nodes')
    return result.fetchone()[0]

def num_ways():
    result = cur.execute('SELECT COUNT(*) FROM ways')
    return result.fetchone()[0]

def common_way_tag():
    result = cur.execute('SELECT key, count(*)\
                          FROM ways_tags \
                          GROUP BY 1 \
                          ORDER BY count(*) DESC \
                          LIMIT 1')
    return result.fetchone()[0]

def num_unique_users():
    result = cur.execute('SELECT COUNT(distinct(uid)) \
                          FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways)')
    return result.fetchone()[0]

def num_unique_bars():
    result = cur.execute('SELECT COUNT(distinct id) FROM nodes_tags WHERE value="bar"')
   
    return result.fetchone()[0]

def num_unique_schools():
    result = cur.execute('SELECT COUNT(*) FROM nodes_tags WHERE value="school"')
   
    return result.fetchone()[0]

def top_contributer():
    for row in cur.execute('SELECT user, COUNT(*) as num \
                            FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) user \
                            GROUP BY user \
                            ORDER BY num DESC \
                            LIMIT 1'):
        return row

def most_popular_religion():
    for row in cur.execute('SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags \
                            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i \
                            ON nodes_tags.id=i.id \
                            WHERE nodes_tags.key="religion" \
                            GROUP BY nodes_tags.value \
                            ORDER BY num DESC\
                            LIMIT 1'):
         return row

def most_popular_amenity():
    for row in cur.execute('SELECT value, COUNT(distinct id) as num \
                            FROM nodes_tags \
                            WHERE key="amenity" \
                            GROUP BY value \
                            ORDER BY num DESC \
                            LIMIT 1'):
        return row

                
if __name__ == '__main__':

    con = sqlite3.connect("bothell.db") 
    cur = con.cursor()
    print ("Number of nodes: " , num_nodes())
    print ("Number of ways: " , num_ways())
    print ("Most Common Way: " , common_way_tag())
    print ("Number of unique users: " , num_unique_users())
    print ("Number of unique bars: " , num_unique_bars())
    print ("Number of unique schools: " , num_unique_schools())
    print ("Top Contributing user: " , top_contributer())
    print ("Biggest religion: " , most_popular_religion())
    print ("Most popular amenity: " , most_popular_amenity())

  