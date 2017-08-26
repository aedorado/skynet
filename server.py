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
import hashlib
import Trie
import difflib
import bisect
import Queue
import threading
import FileServer

persist_port = 9996                   # set port where persistence is listening
persist_ip = '172.20.52.8'             # set ip of persistence
master_ip1 = '172.20.52.8'              # set ip of master
files_path = '/home/placements2018/Music'


char_to_int = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15,'g':16}

BUFFER = 4096
count = 0

def tester(self,key):
	print "testing func ",self.mental,key

def update_trie(self, filename,master_ip) :
	print "hey  uuuuuoo"
	print filename,"master_ip :",master_ip
	soc_conn_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print filename
	print self.MASTER_HOST
	self.MASTER_PORT = self.MASTER_PORT

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

	ip_ob = IP.IP()
	my_ip = ip_ob.get_my_ip()
	#self.ip = my_ip
	#---------------------------------
	my_ip = master_ip1         # ip of master

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
			#reply = 'OK...' + data


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
				file_server.setSharedDirectory(files_path)
				file_server.startServer()

				print "sending to client : ",message
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
				filename_key = data[data.rfind(':')+1:]
				print "filename_key",filename_key
				#update_trie(self, filename)


				masters_list = get_masters_from_persistence("server 2:LIST_OF_MASTERS")
				list_of_masters = masters_list.split()
				print "list of masters :" , list_of_masters,"PPPPPPPPP"

				for master_ip in list_of_masters:
					update_trie(self, filename_key, master_ip)       # later not to store ip beacuse trie on master will just have the file names
					#tester(self,"666666")

				print "Updated trie in all masters"					
	
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

			elif data[:3] == '22:' :
				print "Pastry search protocol"
				filekey = data[data.rfind(':')+1:]
				print "filekey :",filekey
				step = 0
				for i in range(0,min(len(self.nodeid),filekey)):
					if(self.nodeid[i] != filekey[i]):
						break
					else:
						step += 1
				print "current matching steps :",step
				target_ip = client_back_process(self,conn,filekey,str(step))
				return target_ip

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

	host = persist_ip
	print "connecting to persistence : ",host
	#---------------------------------

	port = persist_port                # port where persistence is listening

	s.connect((host, port))
	print "connected server to persis to get master"
	
	s.send(message)
	print "hey 000"

	masters_list = s.recv(1024)
	#print "heuu ",masters_list
	s.close()
	print('connection closed')
	return masters_list


def client_back_process(self,conn,filekey,step):
	global BUFFER

	#here should be added a try catch block - to detect lost connecions or failed connections
	try :
		step_next = str(int(step) + 1)


		check = self.check_information(self.nodeid,step)


		print "checking done :",check

		message = ""

		if(check is not "NULL"):         ###########------ checking the leaf and routing --------
			closest_peer = get_masters_from_persistence("server IP_FROM_ID:"+ str(check))
			#closest_peer = get_masters_from_persistence("server IP_FROM_ID:"+ "a4db03a4fae6df7531f99060a4d2751d14e78805")   # for dummy check
			try:                                # to forward the request to the next peer
				print "forwarding the request to ",closest_peer

				## ------------- find closest_peer's ip using routingtable and leaf set ???---------

				queue = Queue.Queue() 
				thread = threading.Thread(target=self.client_front_process, args=(filekey,closest_peer,queue))
				thread.start()     
				thread.join()
				message = queue.get()

			except Exception, errtxt:
				print errtxt

		else:
			message = self.ip
			print "only one :",message

		print "sending the collective message : ",message
		while  True:
			try :
				conn.sendall(message)
			except socket.error:
				print 'Send failed and retrying'
				continue
			finally :
				break
		#conn.sendall(reply)
		conn.close()
	except Exception, errtxt:
		print errtxt
	#conn.sendall(reply)
	 
	#came out of loop
	conn.close()


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

			#peer_ip = data[data.rfind('>') + 1:data.rfind(':')]    # client ip from whom search started
			#peer_nodeid = hashlib.sha1(peer_ip).hexdigest()

			print data
			peer_nodeid = data[data.rfind('>') + 1:data.rfind(':')]

			step = data[data.rfind(':') + 1:]          # step to know which row of 

			if(step == "-1"):
				step = self.number_of_matching_digits(peer_nodeid)
				print "Now step is : ",step
														 # its routing table to be returned
			print "^^ ",step 
			step_next = str(int(step) + 1)

			if data.find("REQUEST") is not -1:

				print "Request query from the peer with ip : ",addr

				check = self.check_information(peer_nodeid,step)


				print "checking done :",check

				message = ""

				if(check is not "NULL"):         ###########------ checking the leaf and routing --------
					closest_peer = get_masters_from_persistence("server IP_FROM_ID:"+ str(check))
					#closest_peer = get_masters_from_persistence("server IP_FROM_ID:"+ "a4db03a4fae6df7531f99060a4d2751d14e78805")   # for dummy check
					try:                                # to forward the request to the next peer
						print "forwarding the request"
						msg_to_send = "REQUEST INTERMEDIATE <ip>"+ peer_nodeid +":"+step_next

						print "msg to send :",msg_to_send
						print "closest peer :",closest_peer
						## ------------- find closest_peer's ip using routingtable and leaf set ???--------- 

						queue = Queue.Queue()
						thread_ = threading.Thread(target=self.peer_front_process, args=(msg_to_send,closest_peer,queue))
						     # Separate thread to accept the incoming connections from tier 2 peers
						thread_.start()
						thread_.join()
						message = queue.get()
					except Exception, errtxt:
						print errtxt

				else:
					print "sending back the leaves"

					
					message = message + "&"
					for lf in self.leaf:                  # sending leaf set back from the Z node
						message = message + " " + lf
					message = message + " #"

				print "sendinf the routing table rows"
				print len(self.routing)," ",int(step)
				message = message + "Routing "
				#print "ey uu ",step

				if(len(self.routing) > int(step)):
				#	print ":) :) "
					#message = message + " ROUTING: ^"
					for cols in self.routing[int(step)]:
						message = message + " " + cols	

				message = message +" ^ "+self.nodeid
 
				if data.find("START") is not -1:               # to check if this is the A peer
					print "The node was starting node so send neighbours"
					message = message + "$ "
					if(len(self.neighbour) > 0):
						print "getting the neight"	
						for neig in self.neighbour:
								message = message + " " +  neig
					message = message + "@"+str(step)

				print "Updating the Routing table with peer having match of : ",step
				curr_size = len(self.routing)
				#curr_size = 
				print "curr size :" ,curr_size," Table is : ",self.routing
				for i in range(curr_size,int(step)+2):
					print "pushing the row : ",i
					self.routing.append(["NULL"]*20)
				print "here i m : ",self.routing
				print "Now : ",char_to_int[peer_nodeid[int(step)]]," ",peer_nodeid[int(step)]," ",int(step)," ",peer_nodeid
				self.routing[int(step)][char_to_int[peer_nodeid[int(step)]]] = peer_nodeid   # updating the routing table of cuurent node with the joining peer id
				
				print "Updating leaf set with peer having match of : ",step
				bisect.insort(self.leaf,peer_nodeid)
				if(self.nodeid > peer_nodeid):
					self.leaf = self.leaf[1:]
				else:
					self.leaf = self.leaf[:-1]
				print "Leaf set after updation ",self.leaf

				print "Table after updation"
				for i in range(0,len(self.routing)):
					for j in range(0,len(self.routing[i])):
						print self.routing[i][j], " ",
					print "\n"

				print "sending the collective message : ",message
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
			#conn.sendall(reply)
	except Exception, errtxt:
		print errtxt
		conn.close()
	#conn.sendall(reply)
	 
	#came out of loop
	#conn.close()


class Server :
	def __init__(self, server_port, peer_forward_port, peer_backward_port, client_forward_port, client_backward_port, master_port) :

		#create id of server using the hash of IP address and MAC
		self.HOST = ''   # Symbolic name meaning all available interfaces
		#self.PORT = 9167 # All servers will listen on this port -- to listen to CLIENTS
		#self.PEER_PORT = 9570 # to listen to PEERS
		#self.MASTER_PORT = 11500
		self.PORT = int(server_port)
		self.PEER_HOST = ""
		self.PEER_FORWARD_PORT = int(peer_forward_port)
		self.PEER_BACKWARD_PORT = int(peer_backward_port)
		self.CLIENT_FORWARD_PORT = int(client_forward_port)
		self.CLIENT_BACKWARD_PORT = int(client_backward_port)
		self.MASTER_PORT= int(master_port)
		self.MASTER_HOST = ""
		self.PORT_Mapper = port_mapper.PortMap()
		self.ip = ""
		self.nodeid = ""
		self.A_server = ""

		# Pastry protocol datastructures :--------
		self.leaf = []       # contain Leaf nodes having L/2 closest small and L/2 closest greater nodes
		self.neighbour = []  # contain neighbours - k closest nodes according to the proximity measure
		self.routing = []    # routing table

		for i in range(0,20):
			self.routing.append(["NULL"]*20)

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


		#self.nodeid = "abc8960"      # dummy nodeid

		self.HOST = self.ip

		#self.leaf = ["abc4550","cd4562"]
		#self.neighbour = ["35abce", "f538ab"]
		#temp = ["NULL"]*16
		#print self.routing
		#self.routing.append(temp)
		#self.routing.append(temp)
		#self.routing.append(temp)
		#self.routing.append(temp)
	#	print self.check_information("3496fe",3) 

		#print "getting list of masters :"
		#masters_list = get_masters_from_persistence("server 2:LIST_OF_MASTERS")
		#print "99 ",masters_list
		#exit()

		self.register_to_persistence()
		#get_masters_from_persistence("server 2:LIST_OF_MASTERS")

		

		if self.A_server is "0" :                         # decide this condition of master selection later
			print "I am the first peer in the network"
		else:	
			try:
				queue = Queue.Queue()
				thread_ = threading.Thread(target=self.peer_front_process, args=("REQUEST START<id>" +self.nodeid + ":-1",self.A_server,queue))
				thread_.start()     # Separate thread to accept the incoming connections from tier 2 peers
				# decoding the received data after the search process done
				thread_.join()
				msg = queue.get()
				print "Decoding the data : ",msg
				leaf = msg[msg.rfind('&')+1:msg.rfind('#')]

				leaf = leaf.strip()
				self.leaf = leaf.split()
				print "leaf is : ",self.leaf

				nei = msg[msg.rfind('$')+1:msg.rfind('@')]
				nei = nei.split()
				print "Neighbour is : ", self.neighbour

				step = msg[msg.rfind('@')+1:]
				step = int(step)

				routing = msg[msg.rfind('#')+1:msg.rfind('$')]
				routing = routing.strip()
				routing = routing.split('Routing')

				nodes_on_path = []
				#self.routing = []
				#for i in range(0,step):
				#	self.routing.append(["NULL"]*20)

				print "Debugging : ",self.routing

				for i in range(1,len(routing)):
					x = routing[i].strip()
					row = x[:x.rfind('^')].strip()
					node = x[x.rfind('^')+1:].strip()
					nodes_on_path.append(node)
					entries = row.split()
					for j in range(0,20):	
						self.routing[step][j] = entries[j]        # debugging1
					#self.routing.append(entries)
					#print "hey ",i+1
					#print node, " ",row," ",entries
				
				print "Routing table : "
				print self.routing		

				print "Updating the leaf set :"
				for node in nodes_on_path:
					bisect.insort(self.leaf,node)
					if(len(self.leaf) > 4):
						if(self.nodeid > node):
							self.leaf = self.leaf[1:]
						else:
							self.leaf = self.leaf[:-1]
				print "leaf set after updation :"
				print self.leaf


			except Exception, errtxt:
				print errtxt
		
		self.bind_and_serve()                 # communication with peers and clients after server creation
		
		print 'Super Outside'
		

	def number_of_matching_digits(self,peer_nodeid):
		i = 0;
		l1 = len(self.nodeid)
		l2 = len(peer_nodeid)
		while(i<min(l1,l2)):
			if(self.nodeid[i]!=peer_nodeid[i]):
				break
			i += 1
		return str(i)	

	def check_information(self,peer_nodeid,step):
		l = len(self.leaf)
		if(l==1):
			return self.leaf[0]

		if(l>1 and peer_nodeid>=self.leaf[0] and peer_nodeid<=self.leaf[l-1]):
			return min(self.leaf, key=lambda v: len(set(peer_nodeid) ^ set(v)))
			#return difflib.get_close_matches(peer_nodeid, self.leaf,1)


		print char_to_int[peer_nodeid[int(step)]]
		if(len(self.routing) > step):
			return self.routing[int(step)][char_to_int[peer_nodeid[int(step)]]]              # sending the entry from routing table
		return "NULL"


	def register_to_persistence(self):
		s = socket.socket()             # Create a socket object
		
		host = persist_ip
		port = persist_port                # Reserve a port for your service.

		s.connect((host, port))

		message = " 1:JOIN server"  # message format to join
		#message = raw_input()              # get message as input from terminal
		s.send(message)

		msg = s.recv(1024)
		self.nodeid = msg[:msg.rfind(':')]
		self.A_server = msg[msg.rfind(':')  + 1:]     # ip of A server
		print msg

		s.close()
		print('connection closed')


	def peer_front_process(self,msg_to_send,closest_peer_ip,queue) :
		data = ""
		print "Forwarding the message to the closest peer for peer"
		self.soc_conn_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while True :
			try :
				print "closest peer is : ",closest_peer_ip
				self.soc_conn_peer.connect((closest_peer_ip, self.PEER_BACKWARD_PORT))
			except :
				print 'Unable to connect. Retrying  after 100 millisecinds ..'
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
		queue.put(data)
		self.soc_conn_peer.close()

	def client_front_process(self,msg_to_send,closest_peer_ip,queue) :
		data = ""
		print "Forwarding the message for client  to the closest peer "
		self.soc_conn_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while True :
			try :
				print "closest peer for client is : ",closest_peer_ip
				self.soc_conn_client.connect((closest_peer_ip, self.CLIENT_BACKWARD_PORT))
			except :
				print 'Unable to connect. Retrying (client) after 100 millisecinds ..'
				time.sleep(0.1)
				continue
			finally :
				break

		while True :
			try :
				self.soc_conn_client.sendall(msg_to_send)
			except socket.error:
				print 'Send failed client' 
				continue
			finally :
				break

		data = self.soc_conn_client.recv(4096)
		queue.put(data)
		self.soc_conn_client.close()


	def peer_back_thread(self):
		print "Accepting to peer servers"
		self.socket_obj.update({'port_for_back' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		print "Back port created"

		#Bind socket to local host and port for listening to peers of tier 2
		while True :
			try:
				self.socket_obj['port_for_back'].bind((self.HOST, self.PEER_BACKWARD_PORT))
			except socket.error as msg:
				print 'Bind failed. Error Code'
				continue
			finally :
				break

		self.socket_obj['port_for_back'].listen(10)

		while True:
			conn, addr = self.socket_obj['port_for_back'].accept()
			print 'Connected @ peer ... with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self, addr[0]]			
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(peer_back_process ,(bundle,))


	def client_back_thread(self):
		print "Accepting to query from servers for client"
		self.socket_obj.update({'client_port_for_back' : socket.socket(socket.AF_INET, socket.SOCK_STREAM)})

		print "Back client port created"

		#Bind socket to local host and port for listening to peers of tier 2
		while True :
			try:
				self.socket_obj['client_port_for_back'].bind((self.HOST, self.CLIENT_BACKWARD_PORT))
			except socket.error as msg:
				print 'Bind failed. Error Code'
				continue
			finally :
				break

		self.socket_obj['client_port_for_back'].listen(10)

		while True:
			conn, addr = self.socket_obj['client_port_for_back'].accept()
			print 'Connected @ peer for client-query ... with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self, addr[0]]			
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(client_back_process ,(bundle,))

	def bind_and_serve(self):
		# ***  here we can make another decision to keep two seperate ports to listen to PEERS and CLIENTS
		# ***  else we can keep same port and complicate the code

		print "Inside server serve .."

		try:
			Thread(target=self.peer_back_thread, args=()).start()     # Separate thread to accept the incoming connections from tier 2 peers
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
	server_obj = Server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],sys.argv[5],sys.argv[6])


if __name__ == "__main__" :
	main()
