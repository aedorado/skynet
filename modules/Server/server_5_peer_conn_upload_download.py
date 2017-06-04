import math
import socket, select, string, sys
import netifaces as ni
import time
import master
from thread import *
from threading import Thread
import port_mapper
import FileServer

'''
Find self ip - import os
f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
your_ip=f.read()


or else
import netifaces as ni
ni.ifaddresses('wlp3so')
ip = ni.ifaddresses('eth0')[2][0]['addr']
'''

#server listens at 8870

BUFFER = 4096

def client_thread(buff):
	global BUFFER

	conn = buff[0]
	self = buff[1]
	used_port = 0
	file_server = ""
	#Sending message to connected client
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	
	#infinite loop so that function do not terminate and thread do not end.
	#here should be added a try catch block - to detect lost connecions or failed connections
	try :
		while True:
			'''here there will be the logic 
				* to respond to interconnection request from another tier2 server (this will be constant connections)
				* the other type of connection may be from clients.. this can be search request, 
				* each client will be connected to the client
				* each upload or download will be done by server initiating a new connection from and to client respectively
			'''
			#Receiving from client
			data = conn.recv(BUFFER)
			print data[:-1] + 'k'
			reply = 'OK...' + data
			print used_port


			# '7:' prefix for connection ... corresponding reply
			# '9:' search request ..   # inverted trie implementation
			# '15:' upload request from client
			if data[:-1] == '' :
				break
			elif data[:2] == '7:' :
				print 'New connection initiated; sending reply'
				message = '8:ACK'
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						continue
					finally :
						break
			elif data[:3] == '14:' :
				#Threaded implementation of file upload
				print 'Threaded implementation of file upload'
				used_port = self.PORT_Mapper.get_port()
				self.PORT_Mapper.use_port(used_port)
				message = '15:port:' + str(used_port)
				file_server = FileServer.FileServer(used_port)
				file_server.setSharedDirectory('/home/arnab/skynet_files')
				file_server.startServer()
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						continue
					finally :
						break
						#break
			elif data[:3] == '16:' :
				#Threaded implementation of file upload
				print 'Threaded implementation of file upload'
				self.PORT_Mapper.free_port(used_port)
				message = '17:ACK:' + str("none")
				file_server.stopServer()
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						continue
					finally :
						conn.close()
						break
			elif data[:3] == '10:' :
				#Threaded implementation of file upload
				print 'Threaded implementation of file upload'
			elif data[:-1] == 'exit':
				print 'connection closed' 
				conn.close()
				break
			#conn.sendall(reply)
	except :
		conn.close()
	finally :
		conn.close()
	#conn.sendall(reply)
	 
	#came out of loop
	#conn.close()


def peer_thread(conn):
	global BUFFER
	#Sending message to connected client
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	
	#infinite loop so that function do not terminate and thread do not end.
	#here should be added a try catch block - to detect lost connecions or failed connections
	try :
		while True:
			'''here there will be the logic 
				* to respond to interconnection request from another tier2 server (this will be constant connections)
				* the other type of connection may be from clients.. this can be search request, 
				* each client will be connected to the client
				* each upload or download will be done by server initiating a new connection from and to client respectively
			'''
			#Receiving from client
			data = conn.recv(BUFFER)
			print data[:-1]
			reply = 'OK...' + data

			if data[:3] == '16:' :
				#Threaded implementation of file upload
				print 'Threaded implementation of file upload'
				self.PORT_Mapper.free_port(used_port)
				message = '17:ACK:' + str("none")
				file_server.stopServer()
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						continue
					finally :
						conn.close()
						break
			elif data[:-1] == 'exit':
				print 'connection closed' 
				conn.close()
				break
			conn.sendall(reply)
	except :
		conn.close()
	#conn.sendall(reply)
	 
	#came out of loop
	#conn.close()





class Server :
	def __init__(self) :
		#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		#create id of server using the hash of IP address and MAC
		self.HOST = ''   # Symbolic name meaning all available interfaces
		self.PORT = 9160 # All servers will listen on this port -- to listen to CLIENTS
		self.PEER_PORT = 9570 # to listen to PEERS
		self.PORT_Mapper = port_mapper.PortMap()

		self.ip = ni.ifaddresses('wlp3s0')[2][0]['addr']
		self.socket_obj = {}

		#bound = self.socket_bind()


		#here a mutex has to be implemented
		#this file should be implemented using a database ...
		#wherein tthe server gets to know that it is the first server 
		#hence must assume responsibility of 'Master'
		fHandle = open('master_stub.txt')
		data = fHandle.read()
		fHandle.close()
		data = data.strip()

		if data == '0' :    # becoming mster
			print "Initiating master"
			master_node = master.Master()   #dine
		else :   # connecting to master
			# as the master writes to this file ... i.e. the database that it is the server
			# but for this file the master will put its ip address .... and read can be done simulaneously..
			# when we generalise the server has to register to all of the servers live at that time 
			# when the server demotes it to a normal server ... it disconnects and this has to be detected my the 
			# reglar tier 2 server
			
			#self.register_to_master(data)
			'''try: #h this creates a different threaad
				Thread(target=self.register_to_master, args=(data,)).start()
			except Exception, errtxt:
				print errtxt'''
		print 'outside'

		
		# try:
		# 	Thread(target=self.bind_and_serve, args=()).start()
		# except Exception, errtxt:
		# 	print errtxt	
		self.bind_and_serve()
		print 'Super Outside'
		



	def register_to_master(self, data) :
		# this has to be decided
		data_array = data.strip().split(',')
		#host = data_array[0]
		host = ''
		port = data_array[1]
		self.soc_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		print data_array


		while True :
			try :
				self.soc_master.connect((host, int(port)))
			except :
				print 'Unable to connect. Retrying after 100 millisecinds ..'
				time.sleep(0.1)
			finally :
				break

		self.soc_master.sendall('1:ip:' + self.ip)
		registered = False

		# this to receive the IP of the address to which it should connect
		while not registered :
			try:
				data = self.soc_master.recv(BUFFER)
				print data
				if data[:2] == "2:" :
					if data[2:-1] == 'None' :  # first server to connect
						registered = True
						self.back = None
						print 'First server'
						#self.front = None
						break
					else :
						self.register_to_peer(data)
						registered = True
						break
					#s.close()
					break
					#change the beginning time for measurement
				else:
					#sleep for sometime to indicate a gap
					time.sleep(0.1)
			except:
				pass
			finally :
				self.soc_master.close()


	
	# this will have furthur complex connection mechanism
	# as is there in Pastry				
	def register_to_peer(self, data) :
		host = data[2:-1]
		#port = 8870

		print host + ' : host'
		self.soc_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while True :
			try :
				self.soc_peer.connect((host, self.PEER_PORT))
			except :
				print 'Unable to connect. Retrying after 10000 millisecinds ..'
				time.sleep(0.1)
			finally :
				break



	def socket_bind(self) :    # this effectively cannot be used anywhere
		#trying to bind
		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})
		#  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket_obj.update({'s_peer' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})
		#self.s_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Socket created'
		
		while False :
			#Bind socket to local host and port
			try:
				self.socket_obj['s'].bind((self.HOST, self.PORT))
				self.socket_obj['s'].listen(10)
				self.socket_obj['s_peer'].bind((self.HOST, self.PEER_PORT))
				self.socket_obj['s_peer'].listen(10)
				#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # to enable resuse ofaddress
				#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# enables reuse of address
			except socket.error as msg:
				print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break
			     
		print 'Socket bind complete and listenning' 
		return True 



	def peer_thread_accept(self):
		self.socket_obj.update({'s_peer' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		while True :
			#Bind socket to local host and port
			try:
				self.socket_obj['s_peer'].bind((self.HOST, self.PEER_PORT))
			except socket.error as msg:
				print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break

		self.socket_obj['s_peer'].listen(10)

		while True:
			#wait to accept a connection - blocking call
			#print 'waiting on accept of peer_thread'
			conn, addr = self.socket_obj['s_peer'].accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			 
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(peer_thread ,(conn,))


	def bind_and_serve(self):
		# ***  here we can make another decision to keep two seperate ports to listen to PEERS and CLIENTS
		# ***  else we can keep same port and complicate the code

		print "Inside server serve .."


		#start_new_thread(peer_thread_accept, ())

		'''try:
			Thread(target=self.peer_thread_accept, args=()).start()
		except Exception, errtxt:
			print errtxt'''

		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		while True :
			#Bind socket to local host and port
			try:
				print 'BINDING .......... SERVER PORT'
				self.socket_obj['s'].bind((self.HOST, self.PORT))
				#self.socket_obj['s'].listen(10)
				#print "inside server"
			except socket.error as msg:
				print 'Bind failed in bind_and_serve. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break
		self.socket_obj['s'].listen(10)
		while True:
			#wait to accept a connection - blocking call
			#print 'waiting at accept of client'
			#print self.socket_obj['s']
			conn, addr = self.socket_obj['s'].accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			 
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			buff = [conn, self]
			start_new_thread(client_thread ,(buff,))


def main() :
	server_obj = Server()
	#server_obj.serve()


if __name__ == "__main__" :
	main()