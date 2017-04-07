from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

home_dir = os.path.expanduser("~")
if not os.path.exists(home_dir + "/skynet_files"):
    os.makedirs(home_dir + "/skynet_files")

authorizer = DummyAuthorizer()
# authorizer.add_user("user", "12345", "/home/giampaolo", perm="elradfmw")
authorizer.add_anonymous(home_dir + "/skynet_files", perm='elradfmwM')
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("", 2121), handler)
server.serve_forever()
