'''
    Simple socket server using threads
'''
 
import socket
import sys
import time
from FileServer import FileServer
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 9001 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    msg = conn.recv(1024)
    print 'From client ' + msg
    conn.send('172.19.17.181')
    
    file_server = FileServer()
    file_server.setSharedDirectory('/home/arnab/skynet_files')
    file_server.startServer()
    msg = conn.recv(1024)
    print msg
#    time.sleep(100)
    file_server.stopServer()

    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
s.close()
