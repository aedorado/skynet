import sqlite3 as db
import datetime, time

class Storage():

	def __init__(self):
		self.conn = db.connect('master.db')
		self.cursor = self.conn.cursor()

	def add_new_server(self, add_ip):
		try:
			query = 'INSERT INTO master_servers (ip) VALUES (?)'
			self.cursor.execute(query, (add_ip, ))
			self.conn.commit()
		except db.IntegrityError:
			self.add_heartbeat(add_ip)

	def add_heartbeat(self, add_ip):
		query = 'UPDATE master_servers SET timestamp=? WHERE ip=?'
		# self.cursor.execute(query, (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), add_ip))
		self.cursor.execute(query, (time.time(), add_ip))
		self.conn.commit()

	def clean(self):
		# must remove outdated entries
		pass