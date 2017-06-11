import socket
from ftplib import FTP

class Client():

	def __init__(self):
		self.MASTER_SERVER_IP = '172.19.17.183'	# GET from persistance
		self.MASTER_SERVER_PORT = 10796

		self.TIER_TWO_SERVER_PORT = 11596
		# self.master_conn = self.get_socket_connection(self.MASTER_SERVER_IP, self.MASTER_SERVER_PORT)
		self.TIER_TWO_SERVER_ADD = self.get_tier_two_ip()
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
			sock_conn.connect((ip_address, port))
			print 'Success\n'
			return sock_conn
		# except :
			print 'Unable to connect'

	def send_file_to_server(self, filename, upload_ip):
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

	def upload_file(self, filename):
		print 'Requesting upload ip'
		tier_2_conn = self.get_socket_connection(self.TIER_TWO_SERVER_ADD, self.TIER_TWO_SERVER_PORT)
		tier_2_conn.sendall("10:upload")
		upload_ip = tier_2_conn.recv(4096)
		# print upload_ip
		upload_ip = upload_ip[upload_ip.rfind(':') + 1:]
		print 'Upload ip received ' + upload_ip + '\n'
		self.send_file_to_server(filename, upload_ip)
		tier_2_conn.close()

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
		fs = self.get_socket_connection(download_ip, self.TIER_TWO_SERVER_PORT)
		fs.sendall('14:Request_FTP_Port')
		ftp_port = fs.recv(1024)
		ftp_port = ftp_port[ftp_port.rfind(':') + 1:]
		print 'Requesting FTP port'
		print ftp_port
		ftp = FTP()
		ftp.connect(download_ip, ftp_port)
		ftp.login()
		saved_file = open('RET_' + filename, "wb")
		ftp.retrbinary("RETR " + filename, saved_file.write)
		fs.sendall('16:Close:')
		fs.close()
		print 'File sucessfully Downloaded.'