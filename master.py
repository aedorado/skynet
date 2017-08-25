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

class Server :
	def __init__(self, master_port) :

		self.MASTER_PORT= int(master_port)            # this is the port where client(3rd tier) and server(2nd tier) will listen
		#self.PORT_Mapper = port_mapper.PortMap()
		self.ip = ""                              
		connection_type = 1
		print "GOING TO INITIALIZE IP ADDRESS"
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

		ip_ob = IP.IP()               # Get the ip of the system (machine_ip for master)
		my_ip = ip_ob.get_my_ip()
		self.ip = my_ip

		self.socket_obj = {}

		self.HOST = self.ip 

		print "Initiating master ",my_ip
		self.master_node = master_8.Master(self.MASTER_PORT)   # creating the master using file master_8.py
	

def main() :
	server_obj = Server(sys.argv[1])     # this argument is simply the port where master will listen to client and server


if __name__ == "__main__" :
	main()
