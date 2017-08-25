
import argparse
from Client import Client
import socket
import IP
import hashlib

persist_port = 9996                     # set port where persistence is listening
persist_ip = '172.20.52.8'              # set ip of persistence

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--upload', type=str, help='Upload the specifired file')
parser.add_argument(
    '-s',
    '--search',
    type=str,
    help='Search for the specified file.')
parser.add_argument(
    '-d',
    '--download',
    type=str,
    help='Download the specified file.')

def connect_to_persistence(message):
    s = socket.socket()             # Create a socket object
    
    host = persist_ip
    port = persist_port

    s.connect((host, port))
    print "connected to persis"

    s.send(message)

    master_ip = s.recv(1024)
    print "heuu ",master_ip
    s.close()
    print('connection closed')
    return master_ip

args = parser.parse_args()

print args.upload

if args.upload:
    c = Client()
    #c.send_file_to_server(args.upload+"<key>"+'567','172.17.14.23')
    msg = connect_to_persistence("client 2:SERVER2")  # 
   # filekey = hashlib.sha1(args.upload).hexdigest()
    server = msg[:msg.rfind(':')]
    filekey = msg[msg.rfind(':')+1:]
    print server," --",filekey
    k_peers = connect_to_persistence("client K-NEAREST:"+filekey)
    k_peers = k_peers.split()
    for peer in k_peers:
        print "sending file to peer : ",peer
        c.send_file_to_server(args.upload+"<key>"+filekey,peer)    # uploading the file in k nearest neighbours


if args.download:
    c = Client()
    file = args.download
    print "Downloading : ",file
    master = connect_to_persistence("client 1:MASTER")     # to get the ip of a random master
    msg = c.query_file(file,master[master.rfind(':')+1:])      # put master ip here to get files list
    filename = msg[msg.rfind(':')+1:]
    file_id = msg[:msg.rfind(':')]
    print "Filekey to download : ",file_id,"-- file name = ",filename
    server = connect_to_persistence("client 2:SERVER1")
    target_ip = c.search_pastry(server,file_id)     # put serverip got from persistence here
    print "Target ip is :",target_ip
    c.download_file(target_ip, filename)

