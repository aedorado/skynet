import socket
from ftplib import FTP

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '172.19.17.181'
port = 9001

file_to_upload = ''

client.connect((host, port))
client.send('7:file_upload_query_location:' + file_to_upload)

upload_address = client.recv(1024)
print 'Upload Location : ' + upload_address

ftp = FTP()
ftp.connect("172.19.17.181", 2121)
ftp.login()
fh = open("/home/dorado/Downloads/1.mp4", 'rb')
ftp.storbinary('STOR ww.mp4', fh)

client.send('HELLO')

client.close()
