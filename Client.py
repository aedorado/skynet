import socket
from ftplib import FTP

class Client():

	def __init__(self):
		self.MASTER_SERVER_IP = '10.0.0.4'	# GET from persistance
		self.MASTER_SERVER_PORT = 3001

		self.TIER_TWO_SERVER_PORT = 2756
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
			sock_conn.connect((ip_address, port))
			#sock_conn.connect(('172.26.35.147', 2039))
			print 'Success\n'
			return sock_conn
		# except :
			print 'Unable to connect'

	def send_file_to_server(self, filename, upload_ip):
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
		fh = open(filename, 'rb')
		print 'Uploading ' + filename + '\n'
		ftp.storbinary('STOR ' + filename, fh)
		fs.sendall('16:filename:' + filename)
		fs.close()
		print 'Upload sucessful.'


	#def upload_file(self, filename,server_ip):
	#	print 'Requesting upload ip///////////////////**********'
	#	tier_2_conn = self.get_socket_connection(server_ip, self.TIER_TWO_SERVER_PORT)   # connecting to the ip of server 
		#print "hey"																		 # received from the persistence module 
	#	self.send_file_to_server(filename,server_ip)    #  sending file to the server 
	#	tier_2_conn.close()


	######################----------Leaving for now because not of use------------##################################
	def query_file(self, filename):
		print 'Searching for filename: ' + filename
		master_conn = self.get_socket_connection(self.MASTER_SERVER_IP, self.MASTER_SERVER_PORT)
		master_conn.sendall('20:FILE_QUERY:' + filename)
		json_result = master_conn.recv(8192)
		print json_result
		json_result = json_result[7:]
		json_result = eval(json_result)
		print 'We found the following files for you: '
		for number in json_result.keys():
			print number + ' : ' + json_result[number]['filename']
		print '\nEnter the filename'
		file_id = raw_input()
		print file_id, json_result[file_id]
		master_conn.close()
		self.download_file(json_result[file_id]['ip'], json_result[file_id]['filename'])


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

	