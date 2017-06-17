# File to read the database created 

import sqlite3

conn = sqlite3.connect('master.db')
print "Opened master successfully";

cursor = conn.execute("SELECT * from master_servers")       # to read the table master_servers
for row in cursor:
	print row[0]," ",row[1]

print "Operation done successfully";

print "Opened servertable successfully";

cursor = conn.execute("SELECT * from peer_servers")       # to read the table master_servers
for row in cursor:
	print row[0]," ",row[1]," ",row[2]," ",row[3]

conn.close()