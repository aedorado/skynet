# 172.19.17.189:10611

import argparse
from Client import Client
import socket

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
    #host = '172.17.23.17'
    host = '172.26.35.147'
    port = 11122                 # Reserve a port for your service.

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
    server = connect_to_persistence("client 2:SERVER")  # 
    c.upload_file(args.upload)

if args.download:
    c = Client()
    print "Downloadin"
    master = connect_to_persistence("client 1:MASTER")     # to get the ip of a random master
    print "Master ip ",master
    #c.download_file('10.0.0.4', '1.mp3')

