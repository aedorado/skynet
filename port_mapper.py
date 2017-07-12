import sys, os
import socket

class PortMap:

   def __init__(self):
       self.pmap = {}
       for i in range(20000, 21800):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',i))
        if result == 0: #port is open
           self.pmap[i] = False
        else:  # port is free
           self.pmap[i] = True
       #print self.pmap

   def get_port(self):
       for port in self.pmap.keys():
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           result = sock.connect_ex(('127.0.0.1',port))
           print "Port result %d" %result
           if (self.pmap[port] == True and not result == 0):
               return port

   def use_port(self, i):
       self.pmap[i] = False

   def is_being_used(self, i):
       return self.pmap[i] == False

   def is_free(self, i):
       return self.pmap[i] == True

   def free_port(self, i):
       self.pmap[i] = True

