import socket                   # Import socket module
import IP                       # module to calculate system IP

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 11113                  # Reserve a port for your service.

s.connect((host, port))
ip_obj = IP.IP()                # object for IP class
my_ip = ip_obj.get_my_ip()

#message = " 1:JOIN 1:" + my_ip    # message format to join
message = raw_input()              # get message as input from terminal
s.send(message)

print s.recv(1024)
s.close()
print('connection closed')
