from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
authorizer = DummyAuthorizer()
# authorizer.add_user("user", "12345", "/home/giampaolo", perm="elradfmw")
authorizer.add_anonymous("/home/dorado/work/skynet", perm='elradfmwM')
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("127.0.0.1", 2121), handler)
server.serve_forever()