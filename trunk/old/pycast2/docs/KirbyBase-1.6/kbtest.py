"""Simple test of kirbybase.

"""
import os

from kirbybase import KirbyBase, KBError
import datetime

# Uncomment one or the other of next two lines to switch between multiuser
# and embedded.  If multiuser, make sure you have a kbserver running.
db = KirbyBase()
#db = KirbyBase('client', '127.0.0.1', 44444)

# If table exists, delete it.
if os.path.exists('plane.tbl'):
    db.drop('plane.tbl')

# Create a table.
db.create('plane.tbl', ['name:str','country:str','role:str','speed:int',
 'range:int','began_service:datetime.date', 'still_flying:bool'])

# Insert a bunch of records.
print db.insert('plane.tbl', ['P-51','USA','Fighter',403,1201,
 datetime.date(1943,6,24),True])
print db.insert('plane.tbl', ['P-47','USA','Fighter',365,888,
 datetime.date(1943,3,12),False])
print db.insert('plane.tbl', ['B-17','USA','Bomber',315,1400,
 datetime.date(1937,5,1),True])
print db.insert('plane.tbl', ['Typhoon', 'Great Britain','Fighter-Bomber',
 389,690,datetime.date(1944,11,20),False])
print db.insert('plane.tbl', ['Sptitfire','Great Britain','Fighter',345,
 540,datetime.date(1939,2,18),True])
print db.insert('plane.tbl', ['Oscar','Japan','Fighter',361,777,
 datetime.date(1943,12,31),False])
print db.insert('plane.tbl', ['ME-109','Germany','Fighter',366,514,
 datetime.date(1936,7,7),True])
print db.insert('plane.tbl', ['JU-88','Germany','Bomber',289,999,
 datetime.date(1937,1,19),False])

# Insert a couple of records using a dictionary for the input values.
print db.insert('plane.tbl', {'name': 'FW-190', 'country': 'Germany',
 'role': 'Fighter', 'speed': 399, 'range': 499,
 'began_service': datetime.date(1942,12,1), 'still_flying': False})
print db.insert('plane.tbl', {'name': 'Zero', 'country': 'Japan',
 'role': 'Fighter', 'speed': 377, 'range': 912,
 'began_service': datetime.date(1937,5,15), 'still_flying': True})

# Change all records that have 'Great Britain' in country field to 'England'.
db.update('plane.tbl', ['country'],['Great Britain'],['England'],['country'])

# Now do an update using a dictionary instead of a list.
db.update('plane.tbl', ['recno'],[7],{'speed': 367})

# Delete the FW-190.  Use equality matching (i.e. '=='), instead of regular
# expression matching.
db.delete('plane.tbl', ['name'],['FW-190'], False)

# Remove deleted (i.e. blank) lines from the table.
db.pack('plane.tbl')

# Select all Japanese planes.
print db.select('plane.tbl', ['country'],['Japan'])

# Select all US planes with a speed greater than 400mph.  When specifiying
# selection criteria against numeric fields, you use python comparison
# expressions (i.e. >,<,==,>=,<=).
print db.select('plane.tbl', ['country','speed'],['USA','>400'])

# Select all bombers, but not fighter-bombers.  When specifying selection
# criteria against string fields, you use python regular expression syntax.
print db.select('plane.tbl', ['role'],['^Bomber'])

# Select all planes, sorted by speed in descending order (i.e. fastest first).
# Include only name and speed in the result set.
print db.select('plane.tbl', ['name'],['.*'],['name','speed'],
 sortField='speed',ascending=False)

# Select all planes that entered service before January 1st, 1942, sorted
# by the date they began service.
print db.select('plane.tbl', ['began_service'],
 ['<%s' % datetime.date(1942,1,1)], sortField='began_service')

# Select all planes that are still flying.
print db.select('plane.tbl', ['still_flying'],[True])

# Select all planes.
print db.select('plane.tbl', ['recno'], ['*'])

# Get total number of records in plane table.
print 'Total records: ', db.len('plane.tbl')
