import socket
from Storage import Storage
import sqlite3 as db

def start_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()               # Get local machine name   
	s.bind(('172.17.23.17', 11111))           # for same machine
	s.listen(10)

	stor = Storage()                          # database will be created only once

	while True:
		conn, addr = s.accept()
		msg = conn.recv(1024)
		print msg
		new_ip = addr[0]                 # ip from the addr recieved after connection of master/server
		if msg.find("master") is not -1:
			if msg.find('1:JOIN') is not -1:
			#	new_ip = msg[msg.rfind(':') + 1:]   # finding the ip from the message received
				try:
					stor.add_new_master(new_ip)     # new server added
					conn.send('Master ADDED')
				except:
					print 'Error occured'
					conn.send('Master addition FAILED')				
			elif msg.find('2:HBEAT') is not -1:     
				try:
					stor.add_heartbeat_master(new_ip)      # updating the time when last ping came from the masters/servers
					conn.send('Master Hbeat UPDATED')
				except:
					print 'Error occured'
					conn.send('Master hbeat update FAILED')	
				pass
		elif msg.find("server") is not -1:
			if msg.find('1:JOIN') is not -1:
				print new_ip
				try:
					stor.add_new_server(new_ip)     # new server added
					conn.send('Peer ADDED')
				except:
					print 'Error occured'
					conn.send('Peer addition FAILED')				
			elif msg.find('2:HBEAT') is not -1:     
				try:
					stor.add_heartbeat_server(new_ip)      # updating the time when last ping came from the masters/servers
					conn.send('Peer hbeat UPDATED')
				except:
					print 'Error occured'
					conn.send('Peer Hbeat updation FAILED')	
				pass

		# to add the function for updating the load of ther servers


if __name__ == "__main__":
	start_listening()
