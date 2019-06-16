#!/usr/bin/env python3

import sys
import os
from socketserver import ThreadingTCPServer
from threading import Thread

# add server load packages
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from server.lib.server import AuthServer
from server.lib.server import Users
from server import APP_HOST, APP_PORT, APP_AUTH_DB

# set authentification db
Users.load(APP_AUTH_DB)

# setup threading server
server = ThreadingTCPServer((APP_HOST, APP_PORT), AuthServer)

# get server information
ip, port = server.server_address

# start threading
_server = Thread(target=server.serve_forever)
_server.daemon = True

print("Server started:\n\tHost: %s\n\tPort: %d" % (ip, port))

_server.run()
