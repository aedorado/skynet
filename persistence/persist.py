import socket
from Storage import Storage
import sqlite3 as db

def start_listening():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('172.19.17.98', 11111))
	s.listen(10)

	while True:
		conn, addr = s.accept()
		msg = conn.recv(1024)
		if msg.find('1:JOIN') is not -1:
			new_ip = msg[msg.rfind(':') + 1:]
			print new_ip
			stor = Storage()
			try:
				stor.add_new_server(new_ip)
				conn.send('2:ADDED')
			except:
				print 'Error occured'
				conn.send('3:FAILED')				
		elif msg.find('3:HBEAT') is not -1:
			new_ip = msg[msg.rfind(':') + 1:]
			stor = Storage()
			try:
				stor.add_heartbeat(new_ip)
				conn.send('4:UPDATED')
			except:
				print 'Error occured'
				conn.send('5:FAILED')	
			pass

if __name__ == "__main__":
	start_listening()