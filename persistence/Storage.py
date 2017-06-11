import sqlite3 as db
import datetime, time

class Storage():

	def __init__(self):
		self.conn = db.connect('master.db')
		self.cursor = self.conn.cursor()
		self.cursor.execute('CREATE TABLE master_servers (master_id ,ip, timestamp)')       # table for masters
		self.cursor.execute('CREATE TABLE peer_servers (server_id ,ip, timestamp, load)')   # table for servers


	def add_new_server(self, add_ip):
		try:
			query = 'INSERT INTO peer_servers (ip) VALUES (?)' 
			self.cursor.execute(query, (add_ip, ))
			self.conn.commit()                                     # to save changes
		except db.IntegrityError:
			self.add_heartbeat(add_ip)

	def add_heartbeat_server(self, add_ip):
		query = 'UPDATE peer_servers SET timestamp=? WHERE ip=?'
		self.cursor.execute(query, (time.time(), add_ip))
		self.conn.commit()
     
	def add_load_server(self, add_ip, load):                       # load is number of clients attached
		query = 'UPDATE peer_servers SET load=? WHERE ip=?'
		self.cursor.execute(query, (load, add_ip))
		self.conn.commit()
	
	def add_id_server(self, add_ip, server_id):                       # setting server_id to every server as unique identifier
		query = 'UPDATE peer_servers SET server_id=? WHERE ip=?'
		self.cursor.execute(query, (server_id, add_ip))
		self.conn.commit()

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
		query = 'UPDATE peer_servers SET master_id=? WHERE ip=?'
		self.cursor.execute(query, (master_id, add_ip))
		self.conn.commit()

	def clean(self):
		# must remove outdated entries
		pass
