import socket
from ftplib import FTP
import IP

mast_port = 5011
serv_port = 5012


class Client():

	def __init__(self):
		ip_ob = IP.IP()
		my_ip = ip_ob.get_my_ip()
		self.MASTER_SERVER_IP = my_ip              # put ip of master server here manually 
		self.MASTER_SERVER_PORT = mast_port
		self.TIER_TWO_SERVER_PORT = serv_port           # first port put in case of running of server.py

	'''def get_tier_two_ip(self):
		print 'Requesting Tier 2 IP'
		master_conn = self.get_socket_connection(self.MASTER_SERVER_IP, self.MASTER_SERVER_PORT)
		master_conn.sendall('5:REQUEST_TIER_2_ADDRESS:')
		t2ip = master_conn.recv(1024)
		t2ip = t2ip[t2ip.rfind(':') + 1:]
		print 'Success Tier 2 ip is : ' + t2ip + '\n' 
		return t2ip
		master_conn.close()
	'''

	def get_socket_connection(self, ip_address, port):
		print 'Attempting connection to ' + ip_address + ' on port ' + str(port)
		if True:
			sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print "socket created"
			sock_conn.connect((str(ip_address), int(port)))
			print 'Success\n'
			return sock_conn

	def send_file_to_server(self, filename_key, upload_ip):
		upload_ip = str(upload_ip)
		fs = self.get_socket_connection(upload_ip, self.TIER_TWO_SERVER_PORT)
		fs.sendall('14:Request_FTP_Port')
		print 'FTP port request sent'
		ftp_port = fs.recv(1024)
		print "checking " ,ftp_port
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


	def query_file(self, filename, master_ip):
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
		master_conn.close()
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

	def search_pastry(self,server,filekey):
		fs = self.get_socket_connection(server, self.TIER_TWO_SERVER_PORT)
		print "Requesing the file with filekey : ",filekey
		fs.sendall('22:Request_the_target :'+filekey)
		target_ip = fs.recv(1024)
		print "testing arget ",target_ip
		fs.close()
		return target_ip
	
