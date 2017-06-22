import socket
from ftplib import FTP
import IP

class Client():

	def __init__(self):
		# just to show to bibhas sir-----
		ip_ob = IP.IP()
		my_ip = ip_ob.get_my_ip()
		#self.ip = my_ip
		self.MASTER_SERVER_IP = my_ip
		#---------------------------------
		#self.MASTER_SERVER_IP = 	# GET from persistance
		
		self.MASTER_SERVER_PORT = 4077

		self.TIER_TWO_SERVER_PORT = 4071    # first port put in case of server.py
		# self.master_conn = self.get_socket_connection(self.MASTER_SERVER_IP, self.MASTER_SERVER_PORT)
		#self.TIER_TWO_SERVER_ADD = self.get_tier_two_ip()
		# self.tier_2_conn = self.get_socket_connection(self.TIER_TWO_SERVER_ADD, self.TIER_TWO_SERVER_PORT)
		# self.TIER_TWO_SERVER_PORT = 10619

	def get_tier_two_ip(self):
		print 'Requesting Tier 2 IP'
		master_conn = self.get_socket_connection(self.MASTER_SERVER_IP, self.MASTER_SERVER_PORT)
		master_conn.sendall('5:REQUEST_TIER_2_ADDRESS:')
		t2ip = master_conn.recv(1024)
		t2ip = t2ip[t2ip.rfind(':') + 1:]
		print 'Success Tier 2 ip is : ' + t2ip + '\n' 
		return t2ip
		master_conn.close()

	def get_socket_connection(self, ip_address, port):
		print 'Attempting connection to ' + ip_address + ' on port ' + str(port)
		# try :
		if True:
			sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "socket created"
			#print "Now connecting to : ",ip_address," && ",port
			sock_conn.connect((str(ip_address), int(port)))
			#sock_conn.connect(('172.17.14.2',4034))
			#sock_conn.connect(('172.26.35.147', 2039))
			print 'Success\n'
			return sock_conn
		# except :
			print 'Unable to connect'

	def send_file_to_server(self, filename_key, upload_ip):
		upload_ip = str(upload_ip)
		fs = self.get_socket_connection(upload_ip, self.TIER_TWO_SERVER_PORT)
		fs.sendall('14:Request_FTP_Port')
		print 'FTP port request sent'
		ftp_port = fs.recv(1024)
		ftp_port = ftp_port[ftp_port.rfind(':') + 1:]
		print 'FTP port received : ' + str(ftp_port)
		ftp = FTP()
		ftp.connect(upload_ip, ftp_port)
		ftp.login()
		filename = filename_key[:filename_key.rfind('<')]
		fh = open(filename, 'rb')
		print 'Uploading ' + filename + '\n'
		ftp.storbinary('STOR ' + filename, fh)
		fs.sendall('16:filename:' + filename_key)
		fs.close()
		print 'Upload sucessful.'


	#def upload_file(self, filename,server_ip):
	#	print 'Requesting upload ip///////////////////**********'
	#	tier_2_conn = self.get_socket_connection(server_ip, self.TIER_TWO_SERVER_PORT)   # connecting to the ip of server 
		#print "hey"																		 # received from the persistence module 
	#	self.send_file_to_server(filename,server_ip)    #  sending file to the server 
	#	tier_2_conn.close()


	def query_file(self, filename,master_ip):
		filename = filename.lower()
		print 'Searching for filename: ' + filename
		master_conn = self.get_socket_connection(master_ip, self.MASTER_SERVER_PORT)
		master_conn.sendall('20:FILE_QUERY:' + filename)
		json_result = master_conn.recv(8192)
		print json_result
		json_result = json_result[7:]
		json_result = eval(json_result)
		print 'We found the following files for you: '
		for number in json_result.keys():
			print number + ' : ' + json_result[number]['filename'] 
		print '\nEnter the filename serial no. :'
		file_id = raw_input()
		file_id = file_id.lower()
		#print file_id,"***", json_result[file_id]
		master_conn.close()
		#self.download_file(json_result[file_id]['ip'], json_result[file_id]['filename'])
		return json_result[file_id]['id']+":"+json_result[file_id]['filename']

	def download_file(self, download_ip, filename):
		print "Downloading the file :"
		fs = self.get_socket_connection(download_ip, self.TIER_TWO_SERVER_PORT)
		fs.sendall('14:Request_FTP_Port')
		ftp_port = fs.recv(1024)
		ftp_port = ftp_port[ftp_port.rfind(':') + 1:]
		print 'Requesting FTP port'
		ftp = FTP()
		ftp.connect(download_ip, ftp_port)
		ftp.login()
		print "client login successful !!"
		saved_file = open(filename, "wb")
		ftp.retrbinary("RETR " + filename, saved_file.write)
		fs.sendall('16:Close:')
		fs.close()
		print 'File sucessfully Downloaded.'

	'''def search_pastry(self,server,filename):
		fs = self.get_socket_connection(server, self.TIER_TWO_SERVER_PORT)
		filekey = ?????
		fs.sendall('22:Request_the_target :'+filekey)
		target_ip = fs.recv(1024)
		fs.close()
		return target_ip
'''


#c = Client()
#sc = c.get_socket_connection('172.17.14.2',4034)
	