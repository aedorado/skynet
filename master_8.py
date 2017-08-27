import math
import traceback
import socket, select, string, sys
sys.path.insert(0, '../Find_IP/')
sys.path.insert(0, '../Trie/')
import netifaces as ni
from random import randint
from thread import *
from threading import Thread
import port_mapper
import socket                   # Import socket module
import IP                       # module to calculate system IP
import Find_IP
import Trie
import json
from random import randint

BUFFER = 4096

persist_port = 9996        # set port where persistence is listening
persist_ip =  '172.20.52.8'             # set ip of persistence


def slave_thread(bundle):
	global BUFFER
	conn = bundle[0]
	self = bundle[1]

	#Sending message to connected client
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	ip_current_server = ""
	ip_server_id = 0

	print "At master handler"
	#infinite loop so that function do not terminate and thread do not end.
	#here should be added a try catch block - to detect lost connecions or failed connections
	try :
	#if True :
		while True:
			#print conn
			#Receiving from client
			print "i am indide..."
			data = conn.recv(BUFFER)
			print data
			print "kkk"
			print  data[:3] == '20:'
			print data[:3]

			#reply = 'OK...' + data
			print self.CONNECTION
			if data[:2] == '1:' :
				print data
				if data[data.rfind(':') + 1:] in self.CONNECTION :    # this is updating server ip
					ip_current_server = data[data.rfind(':') + 1:]
					self.CONNECTION[ip_current_server] = 1
					self.tier_two_server_count += 1
				else :
					ip_current_server = data[data.rfind(':') + 1:]
					self.CONNECTION.update({ip_current_server : 1}) # 1 means that it is connected
					#self.tier_two_server_count += 1

				#conn.sendall('2:ip:' + self.last_ip)  # sending ip to which the tier 2 server should connect
				message = '2:peer_ip:' + self.last_ip
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						conn.close()
						break
						#ontinue
					finally :
						break
				#update last ip
				print data
				self.last_ip = data[data.rfind(':') + 1:] 
				print "self.last_ip :::::: " + self.last_ip
				break
			elif data[:2] == '5:' :   # this is for sending message to client whom to connect with
				#handling connections from clients
				print "i was here"
				keys = self.CONNECTION.keys()  # because connection contains the information ... "ip" : 0/1
				length = len(keys)
				print keys
				selected_key  = keys[randint(0,length-1)]
				print self.CONNECTION
				print selected_key   
				message = "6:connect_to:" + selected_key
				print message
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						conn.close()
						break
						#ontinue
					finally :
						break
				conn.close()
				break
			elif data[:3] == '10:' :  # JUST ......... TO ..... TEST
				#Threaded implementation of file upload
				print 'Threaded implementation of file upload'
				message = '10:ACK:' + str("172.19.17.183") 
				while  True:
					try :
						#Set the whole string
						conn.sendall(message)
					except socket.error:
						#Send failed
						print 'Send failed and retrying'
						conn.close()
						break
						#ontinue
					finally :
						break
			elif data[:3] == "18:" :
				print 'Updating Trie'
				message = '19:ACK:trie_updated'
				filename = data[data.rfind(':') + 1:]
				print message
				self.Trie_obj.insert(filename) 
				print "IN MASTER TRIE HANDLER"
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
				break
			elif data[:3] == '20:' :
				print 'Search Trie'
				filename = data[data.rfind(':') + 1:]
				#print message
				print "filename is : ",filename
				result_dic = self.Trie_obj.search_get_json(filename) 
				print "result_dic = ",result_dic
				message = '21:ACK:' + json.dumps(result_dic)
				print message
				print "IN MASTER TRIE QUERY HANDLER"
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
				break
			elif data[:-1] == 'exit':
				print 'connection closed' 
				conn.close()
				del self.CONNECTION[ip_current_server]
				self.tier_two_server_count -= 1
				#del self.CONNECTION[data[5:-1]]
				conn.close()
				break
			#conn.sendall(reply)
			print data
	except  Exception, excep :
		print 'problem detected'
		self.CONNECTION[ip_current_server] = 0   # 0 means disconnected  .. this is to be updated onto a database
		self.tier_two_server_count -= 1
		conn.close()
	#conn.sendall(reply)
	print "Exiting" 
	#came out of loop
	#conn.close()

#master listens at 10560

class Master :
	def __init__(self, port) :

		#create id of server using the hash of IP address and MAC
		self.HOST = ''   # Symbolic name meaning all available interfaces
		self.PORT = int(port)

		
		self.tier_two_server_count = 0
		self.ip = ""
		connection_type = 1
		while True :
			try :
				if connection_type == 1 :
					self.ip = ni.ifaddresses('enp1s0')[2][0]['addr']
				else :
					self.ip = ni.ifaddresses('eth0')[2][0]['addr']
			except :
				self.ip = ni.ifaddresses('eth0')[2][0]['addr']
			finally :
				break

		# checking ^^^^
		ip_ob = IP.IP()
		my_ip = ip_ob.get_my_ip()
		self.ip = my_ip
		#---------------------------------


		# variable for initial logic .. 
		# master sends own ip 
		print "MY MASTER IP ::::" + self.ip
		self.last_ip = self.ip
		self.HOST = self.ip

		#print "connecting to persistence in master"
		self.register_to_persistence()

		self.CONNECTION = {self.ip:1}   # this has also to be implemented in a database
		self.CONNECTION_ID = {}   # this has also to be implemented in the same database .. for the ID

		self.socket_objects = []
		print "created trie object"
		self.Trie_obj = Trie.Trie()

		# dummy trie
		#print "creating Dummy trie:"
		#self.Trie_obj.insert("Animal<id>4343")
		#self.Trie_obj.insert("Animals<id>4352")
		#self.Trie_obj.insert("Anima<id>768")
		#self.Trie_obj.insert("Animl<id>998")

		#print self.Trie_obj.search_get_json("Ani")


		#bound = self.socket_bind()   #.. there is a definite pattern to accept request

		#here a mutex has to be implemented
		#this file should be implemented using a database ...
		#since the server creating a master is in actually a master
		#so it must update the file .. i.e the database about its existence
		#fHandle = open('master_stub.txt', 'w')
		#data = fHandle.write(self.ip + ',' + str(self.PORT))
		#print "hyy ",data
		#data = fHandle.write('0')
		#fHandle.close()

		print "yes.. bind.. retuen"
		
		try:
			Thread(target=self.bind_and_serve, args=()).start()
		except Exception, errtxt:
			print errtxt
		
		#start_new_thread(self.bind_and_serve, ())

	def register_to_persistence(self):
		s = socket.socket()             # Create a socket object

		#ip_ob = IP.IP()
		#my_ip = ip_ob.get_my_ip()
		host = persist_ip
		#---------------------------------

		#host = '172.26.35.147'
		#host = '172.17.23.17'
		port = persist_port                 # Reserve a port for your service.

		s.connect((host, port))

		message = " 1:JOIN master"  # message format to join
		#message = raw_input()              # get message as input from terminal
		s.send(message)

		print "Master id : ",s.recv(1024)
		s.close()
		print('connection closed')



	def bind_and_serve(self):
		self.socket_objects += [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
		print 'Socket created   .... master at',self.PORT
		print self.PORT

		while True :
			#Bind socket to local host and port
			try:
				print 'ok'
				self.socket_objects[0].bind((self.HOST, self.PORT))
				print "socket created at ",self.HOST," ",self.PORT
				#conn, addr = self.socket_objects[0].accept()
				#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
			except socket.error as msg:
				print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break

		self.socket_objects[0].listen(10)
		#print "master established...."

		while True:
			#wait to accept a connection - blocking call
			conn, addr = self.socket_objects[0].accept()
			print 'Connected @ master :: with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self]
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(slave_thread ,(bundle,))


def main() :
	master_obj = Master()


if __name__ == '__main__' :
	main()
