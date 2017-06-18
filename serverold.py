import math
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import netifaces as ni
import socket                   # Import socket module
import IP                       # module to calculate system IP
import time
import master_8
from thread import *
from threading import Thread
import port_mapper
import Find_IP
import Trie

import FileServer

BUFFER = 4096
count = 0


def update_trie(self, filename,master_ip) :
	soc_conn_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print filename
	print self.MASTER_HOST
	self.MASTER_PORT = 2045

	while True :
		try :
			soc_conn_master.connect((master_ip, self.MASTER_PORT))
		except :
			print 'Unable to connect. Retrying after 100 millisecinds ..'
			time.sleep(0.1)
		finally :
			break

	message = "18:update_trie:" + filename
	print message + '------------------------------'

	while True :
		try :
			#Set the whole string
			soc_conn_master.sendall(message)
		except socket.error:
			#Send failed
			print 'Send failed server' + message
			continue
			#sys.exit()
		finally :
			break


	print 'Message send successfully to server :: ' + message

	while True :
		try :
			data = soc_conn_master.recv(4096)
			print data + "kkppp"
		except  :
			print 'Recv Failed server' + message
			continue
			#sys.exit()
		finally :
			print data
			break

	soc_conn_master.close()


def client_thread(buff):
	global BUFFER, count
	count += 1

	# just to show to bibhas sir-----
	ip_ob = IP.IP()
	my_ip = ip_ob.get_my_ip()
	#self.ip = my_ip
	#---------------------------------
	#my_ip = "10.0.0.4"         # ip of master
	conn = buff[0]
	self = buff[1]
	used_port = 0
	file_server = ""
	
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
			print "data ",data
			print data[:-1]
			reply = 'OK...' + data


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
				print 'Threaded implementation of file upload'
				used_port = self.PORT_Mapper.get_port()
				print "Get port = %d" %used_port
				self.PORT_Mapper.use_port(used_port)
				message = '15:port:' + str(used_port)
				file_server = FileServer.FileServer(used_port)
				file_server.setSharedDirectory('/home/kritika/Desktop/files')
				file_server.startServer()

				while  True:
					try :
						conn.sendall(message)
					except socket.error:
						print 'Send failed and retrying'
						break
					finally :
						break
						#break
			elif data[:3] == '16:' :
				#Threaded implementation of file upload
				print 'updation of trie after file upload'
				self.PORT_Mapper.free_port(used_port)
				message = '17:ACK:' + str("none")
				file_server.stopServer()
				filename = data[data.rfind(':')+1:]

				#update_trie(self, filename)


				masters_list = get_masters_from_persistence("server 2:LIST_OF_MASTERS")
				list_of_masters = masters_list.split()

				for master_ip in list_of_masters:
					update_trie(self, filename+'<IP>'+my_ip,master_ip)       # later not to store ip beacuse trie on master will just have the file names

				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						continue
					finally :
						count -= 1
						conn.close()
						break
			#elif data[:3] == '10:' :   
			#	print 'Threaded implementation of file upload'
			#	message = '11:IP_address:10.0.0.4'
			#	while  True:
			#		try :
			#			#Set the whole string
			#			conn.sendall(message)
			#		except socket.error:
			#			#Send failed
			#			print 'Send failed and retrying'
			#			continue
			#		finally :
			#			break

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

def get_masters_from_persistence(message):
	s = socket.socket()             # Create a socket object
    #host = '172.17.23.17'
	#host = '172.26.35.147'	
	# just to show to bibhas sir-----
	ip_ob = IP.IP()
	my_ip = ip_ob.get_my_ip()
	#self.ip = my_ip
	host = my_ip
	#---------------------------------

	port = 11117                 # Reserve a port for your service.

	s.connect((host, port))
	print "connected server to persis to get master"
	
	s.send(message)
	print "hey 000"

	masters_list = s.recv(1024)
	print "heuu ",masters_list
	s.close()
	print('connection closed')
	return masters_list


def peer_back_process(bundle):
	global BUFFER

	conn = bundle[0]
	self = bundle[1]
	addr = bundle[2]

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

			peer_ip = data[data.rfind('<ip>') + 1:]    # client ip from whom search started

			if data.find("REQUEST INTERMEDIATE") is not -1:
				step = data[data.rfind(':') + 1:]          # step to know which row of 
														 # its routing table to be returned
				step_next = str(int(step) + 1)

				print "Request query from the peer with ip : ",addr[0]

				if( ----- ):         ###########------ checking the leaf and routing --------

					try:                                # to forward the request to the next peer
						msg_to_send = "REQUEST INTERMEDIATE <ip>"+ peer_ip +" :"+step_next

						## ------------- find closest_peer's ip using routingtable and leaf set ???--------- 

						message = Thread(target=self.peer_front_process, args=(msg_to_send,closest_peer)).start()     
						message = message + " ^"
						for cols in self.routing[int(step)]:       # send the row of intermediate routing table
							message = message + " " + cols
					except Exception, errtxt:
						print errtxt

				else:
					message = "Leaf:"
					for lf in self.leaf:                  # sending leaf set back from the Z node
						message = message + " " + lf

					message = message + " Routing: ^"
					for cols in self.routing[int(step)]:
						message = message + " " + cols	

				if(step == 0):                             # to check if this is the A peer
					message = message + " Neighbour"	 
					for neig in self.neighbour:
							message = message + neig

				while  True:
					try :
						conn.sendall(message)
					except socket.error:
						print 'Send failed and retrying'
						continue
					finally :
						break
				
			conn.close()
			break
			conn.sendall(reply)
	except :
		print "Prob detected"
		conn.close()
	#conn.sendall(reply)
	 
	#came out of loop
	#conn.close()


class Server :
	def __init__(self, server_port, peer_forward_port, peer_backward_port, master_port) :

		#create id of server using the hash of IP address and MAC
		self.HOST = ''   # Symbolic name meaning all available interfaces
		#self.PORT = 9167 # All servers will listen on this port -- to listen to CLIENTS
		#self.PEER_PORT = 9570 # to listen to PEERS
		#self.MASTER_PORT = 11500
		self.PORT = int(server_port)
		self.PEER_HOST = "10.0.0.4"
		self.PEER_FORWARD_PORT = int(peer_forward_port)
		self.PEER_BACKWARD_PORT = int(peer_backward_port)
		self.MASTER_PORT= int(master_port)
		self.MASTER_HOST = "10.0.0.4"
		self.PORT_Mapper = port_mapper.PortMap()
		self.ip = ""

		# Pastry protocol datastructures :--------
		self.leaf = []       # contain Leaf nodes having L/2 closest small and L/2 closest greater nodes
		self.neighbour = []  # contain neighbours - k closest nodes according to the proximity measure
		self.routing = []    # routing table

		connection_type = 1
		print "GOING TO INITIALIZE IP ADDRESSSSSSSS"
		while True :
			try :
				if connection_type == 1 :
					self.ip = ni.ifaddresses('enp1s0')[2][0]['addr']
				else :
					self.ip = ni.ifaddresses('eth0')[2][0]['addr']
				if self.ip == "" :
					continue				
			except :
				self.ip = ni.ifaddresses('eth0')[2][0]['addr']
			finally :
				break

		self.socket_obj = {}

		# just to show to bibhas sir-----
		ip_ob = IP.IP()
		my_ip = ip_ob.get_my_ip()
		self.ip = my_ip
		#---------------------------------

		self.HOST = self.ip 

		fHandle = open('master_stub.txt')        # write 0 in stub file when starting the network
		data = fHandle.read()
		fHandle.close()
		data = data.strip()

		#print "getting list of masters :"
		#masters_list = get_masters_from_persistence("server 2:LIST_OF_MASTERS")
		#print "99 ",masters_list
		#exit()

#		if data == '0' :                         # decide this condition of master selection later
#			print "Initiating master"
#			self.master_node = master_8.Master(self.MASTER_PORT)  


#		else :  
		print "Initiating Server"
		#self.register_to_persistence()

		### to get ip of A server from persistence
		A_server = 


		try:
			data = Thread(target=self.peer_front_process, args=("REQUEST <ip>" +self.ip + " :0",A_server)).start()     # Separate thread to accept the incoming connections from tier 2 peers
		except Exception, errtxt:
			print errtxt

		###  decode the received data after the search process done??????-------------------------

		self.bind_and_serve()                 # communication with peers and clients after server creation
		
		print 'Super Outside'
		

	def register_to_persistence(self):
		s = socket.socket()             # Create a socket object
		#host = '172.17.23.17'
		
		# just to show to bibhas sir-----
		ip_ob = IP.IP()
		my_ip = ip_ob.get_my_ip()
		#self.ip = my_ip
		host = my_ip
		#---------------------------------

		#host = '172.26.35.147'
		port = 11117                  # Reserve a port for your service.

		s.connect((host, port))

		message = " 1:JOIN server"  # message format to join
		#message = raw_input()              # get message as input from terminal
		s.send(message)

		msg = s.recv(1024)
		A_server = msg[msg.rfind(':') + 1:]
		my_nodeid = msg[:msg.rfind(':') - 1]
		s.close()
		print('connection closed')


	def peer_front_process(self,msg_to_send,closest_peer) :
		data = ""
		print "Forwarding the message to the closest peer"
		self.soc_conn_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while True :
			try :
				self.soc_conn_peer.connect((closest_peer, self.PEER_BACKWARD_PORT))
			except :
				print 'Unable to connect. Retrying after 100 millisecinds ..'
				time.sleep(0.1)
				continue
			finally :
				break

		while True :
			try :
				self.soc_conn_peer.sendall(msg_to_send)
			except socket.error:
				print 'Send failed server' 
				continue
			finally :
				break

		data = self.soc_conn_peer.recv(4096)
		self.soc_conn_peer.close()
		return data


	def peer_back_thread(self):
		print "Accepting to peer servers"
		self.socket_obj.update({'s_forward_peer' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		#Bind socket to local host and port for listening to peers of tier 2
		while True :
			try:
				self.socket_obj['s_backward_peer'].bind((self.HOST, self.PEER_FORWARD_PORT))
			except socket.error as msg:
				print 'Bind failed. Error Code'
				continue
			finally :
				break

		self.socket_obj['s_backward_peer'].listen(10)

		while True:
			conn, addr = self.socket_obj['s_backward_peer'].accept()
			print 'Connected @ peer ... with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self, addr[0]]			
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(peer_back_process ,(bundle,))


	def peer_front_thread(self):
		print "Accepting to peer servers"
		self.socket_obj.update({'s_backward_peer' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		#Bind socket to local host and port for listening to peers of tier 2
		while True :
			try:
				self.socket_obj['s_forward_peer'].bind((self.HOST, self.PEER_BACKWARD_PORT))
			except socket.error as msg:
				print 'Bind failed. Error Code'
				continue
			finally :
				break

		self.socket_obj['s_forward_peer'].listen(10)

		while True:
			conn, addr = self.socket_obj['s_forward_peer'].accept()
			print 'Connected @ peer ... with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self, addr[0]]			
			start_new_thread(peer_front_process ,(,))


	def bind_and_serve(self):
		# ***  here we can make another decision to keep two seperate ports to listen to PEERS and CLIENTS
		# ***  else we can keep same port and complicate the code

		print "Inside server serve .."

		try:
			Thread(target=self.peer_back_thread, args=()).start()     # Separate thread to accept the incoming connections from tier 2 peers
		except Exception, errtxt:
			print errtxt


		try:
			Thread(target=self.peer_front_thread, args=()).start()     # Separate thread to accept the incoming connections from tier 2 peers
		except Exception, errtxt:
			print errtxt


		self.socket_obj.update({'s' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})  # dictionary update for the socket created
																						   # to listen to the clients
	    # This while loop justs binds the server to the socket created
		while True :
			try:
				print 'BINDING TO SERVER PORT',self.HOST," ",self.PORT
				self.socket_obj['s'].bind((self.HOST, self.PORT))
			except socket.error as msg:
				print 'Bind failed in bind_and_serve. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break

		self.socket_obj['s'].listen(10)           # start listening to the clients

		while True:
			conn, addr = self.socket_obj['s'].accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			 
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			buff = [conn, self]
			start_new_thread(client_thread ,(buff,))       # separate thread for each client


def main() :
	server_obj = Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__" :
	main()