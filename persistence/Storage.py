import sqlite3 as db
import datetime, time
import random
import os
import hashlib
import ipaddress

class Storage():

	def __init__(self):
		os.remove('master.db')              # to delete the already created database
		self.conn = db.connect('master.db')
		self.start_nodeid = 1146            # start nodeid for peers
		self.start_filekey = 1146
		self.cursor = self.conn.cursor()
		self.cursor.execute('CREATE TABLE master_servers (master_id ,ip, timestamp)')       # table for masters
		self.cursor.execute('CREATE TABLE peer_servers (server_id ,ip, timestamp, load)')   # table for servers


	def add_new_server(self, add_ip):
		query = 'SELECT COUNT(*) FROM peer_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		#print "size :",rows
		try:
			query = 'INSERT INTO peer_servers (ip,load) VALUES (?,?)' 
			self.cursor.execute(query, (add_ip,0 ))
			self.conn.commit()                                     # to save changes
		except db.IntegrityError:
			self.add_heartbeat(add_ip)

	def if_first_server(self):
		query = 'SELECT COUNT(*) FROM peer_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		return rows

	def add_heartbeat_server(self, add_ip):
		query = 'UPDATE peer_servers SET timestamp=? WHERE ip=?'
		self.cursor.execute(query, (time.time(), add_ip))
		self.conn.commit()
     
	def add_load_server(self, add_ip, load):                       # load is number of clients attached
		query = 'UPDATE peer_servers SET load=? WHERE ip=?'
		self.cursor.execute(query, (load, add_ip))
		self.conn.commit()
	
	def add_id_server(self, add_ip, server_id):                       # setting server_id to every server as unique identifier
		query = 'SELECT COUNT(*) FROM peer_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		query = 'UPDATE peer_servers SET server_id=? WHERE ip=?'
		#self.cursor.execute(query, (server_id, add_ip))           # nodeid using hashlib
		self.cursor.execute(query, (self.start_nodeid, add_ip))            # dummy nodeid
		self.start_nodeid += 96
		self.conn.commit()
		return str(self.start_nodeid - 96)

	def get_first_server(self,new_ip):
		query = 'SELECT ip FROM peer_servers'
		rows = self.cursor.execute(query).fetchall()
		diff = 100000000000000000000000000
		ans = ""
		new_ip = ipaddress.IPv4Address(unicode(new_ip))
		for ip in rows:
			iip = ip[0]
			ip = ipaddress.IPv4Address(unicode(ip[0]))
			new_diff = abs(int(new_ip) - int(ip))
			if(diff > new_diff):
				diff = new_diff
				ans = iip
		return ans

	def get_server(self):
		#print "getting master"
		query = 'SELECT ip FROM peer_servers ORDER BY load'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		#print rows
		return rows

	def get_list_of_masters(self):
		query = 'SELECT ip FROM master_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchall()
		new_list = ""
		for i in rows:
			new_list = new_list + " " + i[0]
		#print new_list
		return new_list

	def add_new_master(self, add_ip):
		try:
			query = 'INSERT INTO master_servers (ip) VALUES (?)' 
			self.cursor.execute(query, (add_ip, ))
			self.conn.commit()                                     # to save changes
		except db.IntegrityError:
			self.add_heartbeat(add_ip)

	def add_heartbeat_master(self, add_ip):
		query = 'UPDATE master_servers SET timestamp=? WHERE ip=?'
		self.cursor.execute(query, (time.time(), add_ip))
		self.conn.commit()

	def add_id_master(self, add_ip, master_id):                       # setting master_id to every master as unique identifier
		query = 'SELECT COUNT(*) FROM master_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		query = 'UPDATE master_servers SET master_id=? WHERE ip=?'
		self.cursor.execute(query, ("100", add_ip))
		self.conn.commit()

	def get_master(self):
		#print "getting master"
		query = 'SELECT COUNT(*) FROM master_servers'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchone()[0]
		query = 'SELECT ip from master_servers ORDER BY RANDOM() LIMIT 1'    # to get a random master from the persistence
		n = random.randint(0,4)
		ip = self.cursor.execute(query).fetchone()[0]
		return ip

	def get_ip_from_nodeid(self,nodeid):
		query = 'SELECT ip FROM peer_servers where server_id = ?'                 # to get the number of rows present in table 
		rows = self.cursor.execute(query,(nodeid,)).fetchone()[0]
		return rows

	def get_filekey(self):
		self.start_filekey += 48
		key = self.start_filekey
		return str(key)

	def get_k_nearest_server(self,filekey):
		query = 'SELECT server_id,ip FROM peer_servers ORDER BY server_id'              # to get the number of rows present in table 
		rows = self.cursor.execute(query).fetchall()
		new_list = ""
		i = 0
		#print rows
		while(i<len(rows)):
			if(filekey>rows[i][0]):
				i += 1
			else:
				break

		if(i>=len(rows)):
			i -= 1

		print rows
		print i
		k = 2
		ind = i
		while(ind>=0 and k>0):
			new_list = new_list + " " + rows[ind][1]
			ind -= 1;
			k -= 1;
		
		ind = i+1
		k = 2
		while(ind<len(rows) and k>0):
			new_list = new_list + " " + rows[ind][1]
			ind += 1;
			k -= 1;
		
		return new_list


	def clean(self):
		# must remove outdated entries
		pass

'''
stor = Storage()

print "Creating dummy table"
#---------Dummy Table---------
stor.add_new_server('172.17.14.23')
#server_id = hashlib.sha1('172.17.14.23').hexdigest()
stor.add_id_server('172.17.14.23','1146')
stor.add_new_server('172.17.14.24')
#server_id = hashlib.sha1('172.17.14.23').hexdigest()
stor.add_id_server('172.17.14.24','1178')
stor.add_new_server('172.17.14.25')
#server_id = hashlib.sha1('172.17.14.23').hexdigest()
stor.add_id_server('172.17.14.25','1141')
stor.add_new_server('172.17.14.26')
#server_id = hashlib.sha1('172.17.14.23').hexdigest()
stor.add_id_server('172.17.14.26','1197')
stor.add_new_server('172.17.14.27')
#server_id = hashlib.sha1('172.17.14.23').hexdigest()
stor.add_id_server('172.17.14.27','2000')
#stor.add_load_server('172.31.1.1',4)
stor.add_new_server('10.0.0.5')
server_id = hashlib.sha1('10.0.0.5').hexdigest()
stor.add_id_server('10.0.0.5',server_id)
#stor.add_load_server('172.31.1.2',2)
stor.add_new_server('10.0.0.7')
server_id = hashlib.sha1('10.0.0.7').hexdigest()
stor.add_id_server('10.0.0.7',server_id)
#stor.add_load_server('172.31.1.3',8)
stor.add_new_server('10.0.0.8')
server_id = hashlib.sha1('10.0.0.8').hexdigest()
stor.add_id_server('10.0.0.8',server_id)
#stor.add_load_server('172.31.1.4',1)
stor.add_new_server('10.0.0.1')
server_id = hashlib.sha1('10.0.0.1').hexdigest()
stor.add_id_server('10.0.0.1',server_id)
#stor.add_load_server('172.31.1.5',3)
stor.add_new_server('10.0.0.4')
server_id = hashlib.sha1('10.0.0.4').hexdigest()
stor.add_id_server('10.0.0.4',server_id)
#stor.add_load_server('172.31.1.6',4)
stor.add_new_server('10.0.0.3')
server_id = hashlib.sha1('10.0.0.3').hexdigest()
stor.add_id_server('10.0.0.3',server_id)
#stor.add_load_server('172.31.1.7',4)
'''

'''print stor.get_first_server('10.0.0.2')'''

#print stor.get_k_nearest_server("1194")
