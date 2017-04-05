import math
import socket, select, string, sys
import netifaces as ni
from random import randint
from thread import *
from threading import Thread

def slave_thread(bundle):
	conn = bundle[0]
	self = bundle[1]

	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	ip_current_server = ""
	ip_server_id = 0
	#infinite loop so that function do not terminate and thread do not end.
	#here should be added a try catch block - to detect lost connecions or failed connections
	try :
		while True:
			#print conn
			#Receiving from client
			data = conn.recv(1024)
			print data
			'''
			try :
				data = conn.recv(1024)
				print len(data) + 'k'
				#if len(data)
			except :
				print "Connection lost kk"
				self.CONNECTION[ip_current_server] = 0
				self.tier_two_server_count -= 1
				#conn.close()
				break
			'''

			#reply = 'OK...' + data
			if data[:5] == '1:ip:' :
				if data[5:-1] in self.CONNECTION :
					ip_current_server = data[5:-1]
					self.CONNECTION[ip_current_server] = 1
					self.tier_two_server_count += 1
				else :
					ip_current_server = data[5:-1]
					self.CONNECTION.update({ip_current_server : 1}) # 1 means that it is connected
					self.tier_two_server_count += 1

				conn.sendall('2:ip:' + self.last_ip)  # sending ip to which the tier 2 server should connect
				#update last ip
				self.last_ip = data[5:-1]
			elif data[:3] == '5:' :   # this is for sending message to client whom to connect with
				#handling connections from clients
				keys = self.CONNECTION.keys()  # because connection contains the information ... "ip" : 0/1
				length = len(keys)
				selected_key  = keys[randint(0,length)]   
				message = "6:" + selected_key
				conn.sendall(message)
				conn.close()
				break
			elif data[:-1] == 'exit':
				print 'connection closed' 
				conn.close()
				del self.CONNECTION[ip_current_server]
				self.tier_two_server_count -= 1
				#del self.CONNECTION[data[5:-1]]
				break
			#conn.sendall(reply)
	except :
		self.CONNECTION[ip_current_server] = 0   # 0 means disconnected  .. this is to be updated onto a database
		self.tier_two_server_count -= 1
		conn.close()
	#conn.sendall(reply)
	 
	#came out of loop
	#conn.close()

#master listens at 10560

class Client :
	def __init__(self) :
		#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# We should use a DNS to query for the host address and host port
		self.OWN_PORT = 12563    # the client should listen on this port
		self.OWN_HOST = ''       # and on one port it should make a connection to the host port of the master
		
		#create id of server using the hash of IP address and MAC
		
		self.HOST = ['']   		 # This contains all the host that are active now ... the method is needed to be known here
		self.MASTER_PORT = 10585 # All servers will listen on this port
		self.SERVER_PORT = 8885
		self.SERVER_HOST = ''  	 # this is to be provided by the Master ..  based on load and hop count (proximity to client)	  


		self.ip = ni.ifaddresses('wlp3s0')[2][0]['addr']
		# variable for initial logic .. 
		self.last_ip = "NULL"

		self.socket_objects = []

		#bound = self.socket_bind()   #.. there is a definite pattern to accept request

		#here a mutex has to be implemented
		#this file should be implemented using a database ...
		#since the server creating a master is in actually a master
		#so it must update the file .. i.e the database about its existence

		print "All the class variables have been initialized"
		#print self
		#self.serve()
		#starting new thread to listen

		try:
			Thread(target=self.bind_and_serve, args=()).start()
			# this is for the client to listen for incoming upload connnections from other servers .. 
		except Exception, errtxt:
			print errtxt

		try :
			# new connection to master
			Thread(target=self.connect_to_server, args=()).start()
		except Exception, errtxt :
			print errtxt

		#start_new_thread(self.bind_and_serve, ())


	'''
	def socket_bind(self) :
		#trying to bind
		self.socket_objects += [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
		print 'Socket created   .... master'
		
		while False :
			#Bind socket to local host and port
			try:
				print 'ok'
				#self.socket_objects[0].bind((self.HOST, self.PORT))
				#self.socket_objects[0].listen(10)
				#conn, addr = self.socket_objects[0].accept()
				#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
			except socket.error as msg:
				print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break
				 
		print 'Socket bind complete and listenning  ....master' 
		return True
	'''

	def connect_to_master(self) :
		sock_conn_master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#sock_conn_master.settimeout(2)

		# connect to remote host
		try :
			sock_conn_master.connect((self.HOST[0], self.MASTER_PORT))
		except :
			print 'Unable to connect'
		sys.exit()

		message = '5:request_ip'

		try :
			#Set the whole string
			sock_conn_master.sendall(message)
		except socket.error:
			#Send failed
			print 'Send failed'
			sys.exit()

		print 'Message send successfully to master'

		try :
			data = sock_conn_master.recv(4096)
		except  :
			print 'Sent Failed'
			sys.exit()

		sock_conn_master.close()

		# data_format of   data = '6:<IP>'
		# else while checking we can do it using data = ''
		self.SERVER_IP = data[2:-1]

		bool_reply = self.connect_to_server(self) 




	def connect_to_server(self):
		connected = self.connect_to_master()

		message = "7:conc:"+str(self.ip)
		
		while True :
			try :
				#Set the whole string
				sock_conn_master.sendall(message)
			except socket.error:
				#Send failed
				print 'Send failed'
				sys.exit()

			print 'Message send successfully to master'

			try :
				data = sock_conn_master.recv(4096)
			except  :
				print 'Sent Failed'
				sys.exit()

			sock_conn_master.close()




	def bind_and_serve(self):
		self.socket_objects += [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]
		print 'Socket created   .... master'

		while True :
			#Bind socket to local host and port
			try:
				print 'ok'
				self.socket_objects[0].bind((self.OWN_HOST, self.OWN_PORT))
				#conn, addr = self.socket_objects[0].accept()
				#self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
			except socket.error as msg:
				print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				continue
			finally :
				break

		self.socket_objects[0].listen(10)

		while True:
			#wait to accept a connection - blocking call
			conn, addr = self.socket_objects[0].accept()
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			
			bundle = [conn, self]
			#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
			start_new_thread(slave_thread ,(bundle,))


def main() :
	client_obj = Client()
	#master_obj.bind_and_serve()
	

	''' # This part was just to checck the flow and design ..
	s_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_check.bind(('', 5962))
	s_check.listen(10)
	conn, addr = s_check.accept()

	data = conn.recv(2048)
	print data

	conn.close()
	'''


if __name__ == '__main__' :
	main()