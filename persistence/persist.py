import socket
from Storage import Storage
import client_persist as cp
import sqlite3 as db

def start_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()               # Get local machine name   
	#s.bind(('172.17.23.17', 11114))           # for same machine
	#s.bind(('10.0.0.4',11114))
	#port_mapper_obj = pm.PortMap()
	#port = port_mapper_obj.get_port()
	s.bind(('172.26.35.147',11122))
	s.listen(10)

	stor = Storage()                          # database will be created only once

	while True:
		stor.add_new_master('162.45.6.1')
		stor.add_new_master('162.45.6.2')
		stor.add_new_master('162.45.6.3')
		stor.add_new_master('162.45.6.4')

		stor.add_new_server('172.31.1.2')
		stor.add_load_server('172.31.1.2',4)
		stor.add_new_server('172.31.1.1')
		stor.add_load_server('172.31.1.1',2)
		stor.add_new_server('172.31.1.3')
		stor.add_load_server('172.31.1.3',8)
		stor.add_new_server('172.31.1.4')
		stor.add_load_server('172.31.1.4',1)
		stor.add_new_server('172.31.1.5')
		stor.add_load_server('172.31.1.5',3)

		conn, addr = s.accept()
		msg = conn.recv(1024)
		print msg
		new_ip = addr[0]                 # ip from the addr recieved after connection of master/server
		if msg.find("master") is not -1:
			#print "master detected"
			if msg.find('1:JOIN') is not -1:
			#	new_ip = msg[msg.rfind(':') + 1:]   # finding the ip from the message received
				master_id = msg[msg.rfind(':') + 1:]		#recieved master_id from the master
				#print "here ",msg
				try:
					stor.add_new_master(new_ip)     # new server added
			#		conn.send('Master ADDED')
					stor.add_id_master(new_ip,master_id) #adding id for the master
					conn.send('Master ADDED WITH its MASTER_ID')
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
			#	print new_ip
				server_id = msg[msg.rfind(':') + 1:]       #recieved server _id from the server
				try:
					stor.add_new_server(new_ip)     # new server added
					stor.add_id_server(new_ip,server_id) #adding id for the server
					conn.send('Peer ADDED WITH its SERVER_ID')
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
			elif msg.find('2:LIST_OF_MASTERS') is not -1:     
				try:
					lis = stor.get_list_of_masters()      # updating the time when last ping came from the masters/servers
					conn.send(lis)
				except:
					print 'Error occured'
					conn.send('list of masters sending FAILED')	
				pass
		elif msg.find("client") is not -1:
			print "client detected"
			print "Creating dummy table :) -----------------"
			
			if msg.find('1:MASTER') is not -1:
				#client_ip = msg[msg.rfind(':') + 1:]       #recieved  client_ip from the server
				try:
					#master_ip =  "heuuooo"
					master_ip = stor.get_master()
					#print "got ip",master_ip
					conn.send('Master ip:'+master_ip)
				except:
					print 'Error occured'
					conn.send('Master allocation failed')
			elif msg.find('2:SERVER') is not -1:
				#client_ip = msg[msg.rfind(':') + 1:]       #recieved  client_ip from the server
				try:
					server_ip = stor.get_server()
					conn.send('Server ip:'+server_ip)
				except:
					print 'Error occured'
					conn.send('Server allocation failed')
				pass
		# to add the function for updating the load of ther servers


if __name__ == "__main__":
	start_listening()

