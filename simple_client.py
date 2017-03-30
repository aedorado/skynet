# import socket
# import sys
from ftplib import FTP

# # s = socket.socket()
# # s.connect(("172.17.23.5", 8888))

ftp = FTP()
ftp.connect("localhost", 2121)
print (ftp.getwelcome())
ftp.login()

fh = open("/home/dorado/Downloads/erdplus-diagram.png", 'rb')
ftp.storbinary('STOR a.png', fh)