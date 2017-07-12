from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer

import socket
from os.path import exists as path_exists
from os.path import getsize 
from multiprocessing import Process 

class FileServer:
    def __init__(self, port):
        self.port = port
        self.sharedDir = ""
        self.is_running = False 
        self.ftp_handler = FTPHandler
        self.connected = 0
        self.bytesTransferred = 0
        self.filesTransferred = 0

    def setSharedDirectory(self, path):
        print "setting started"
        if not path_exists(path):
            raise FileNotFoundError
        print "hey"
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_anonymous(path, perm='elradfmwM')
        self.ftp_handler.authorizer = self.authorizer

    def startServer(self):
        self.server = FTPServer(('', self.port), self.ftp_handler)
        print "process running:"
        self.server_proc = Process(target=self.server.serve_forever)
        self.server_proc.start()
        #self.server_proc.join()
        '''try:
            Thread(target=self.server.serve_forever, args=()).start()
        except Exception, errtxt:
            print errtxt'''
        self.is_running = True 

    def stopServer(self):
        if self.is_running:
            self.server.close_all()
            self.server_proc.terminate()
            self.server_proc.join()
            print ("FTP server stopped")
            del self.server_proc
            self.server_proc = None 
            self.is_running = False 

