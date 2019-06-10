#!/usr/bin/env python

import SocketServer
import socket
import threading
import json
import sys
import os
import hashlib
import modules


APP_ROOT= (os.path.dirname(os.path.realpath(__file__)))

def _log(text):
	print(text)
	
def _rOK(response):
	return json.dumps({ "response": response }) + "\n"
	
def _rERR(err):
	return json.dumps({ "error": err}) + "\n"

def _printHelp():
	pass

class Users:
	users = {}
	
	@staticmethod
	def addUser(user, ps, ip):
		Users.users[user] = { "password": ps, "ip": ip }
		
	@staticmethod
	def user(user):
		if user in Users.users:
			return Users.users[user]
		return None

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
	
class AuthSocketServer(SocketServer.BaseRequestHandler):
	def handle(self):
		self.auth = False
		self.authCount = 0
		self.loop = True;

		cur_thread = threading.current_thread()
		_log("Starting new thread {}".format(cur_thread.name))
		while self.loop:
			try:
                                json_recieve = self.request.recv(2048).strip()
				data = json.loads(json_recieve)
				if not self.handleCommand(data):
					_log("data sent not fit our format")
					self.request.send(_rERR('wrong data format sent'))
			except Exception, ex:
				_log('There is an exception')
				_log(str(ex))
                                _log("json recieved")
                                _log(json_recieve)
				try:
					self.request.send(_rERR('wrong data format sent'))
				except Exception, err:
					_log("Unable to send response : %s" % err)
					break

		threading.current_thread().exit() #close thread

	def handleCommand(self, data):
		if 'command' not in data:
			return False
		else:
			if data['command'] == 'auth' and not self.auth:
				if 'data' not in data:
					self.request.send(_rERR("Auth data not sent"));
				elif ('user' not in data['data']) or ('pass' not in data['data']):
					self.request.send(_rERR("Auth credentials not sent"))
				else:
					auth = self.tryAuth(data['data']['user'], data['data']['pass'])
					if auth:
						self.auth = { "username": data['data']['user'] }
						self.request.send(_rOK("Hello %s" % self.auth['username']))
					else:
						self.request.send(_rERR("Username or password not correct"))
						self.authCount += 1

				if self.authCount >= 5:
					self.loop = False
					self.request.send(_rERR('5 times failed to auth'))
					self.request.close();

			elif data['command'] == 'close':
				self.loop = False
				self.request.close()
			elif self.auth:
				self.handleAuthOk(data);
			elif not self.auth:
				self.request.send(_rERR('Please auth'));
			else:
				self.request.send(_rERR('Unknown command'))
				
			return True

	def tryAuth(self, user, passwd):
		_log("Try to auth: %s" % user)
		uuser = Users.user(user)
		if uuser is not None:
			return hashlib.sha224(passwd).hexdigest() == uuser['password']
		return False

	def handleAuthOk(self, data):
		if ('command' in data):
			act = data['command'].rsplit('.', 1)
			
			if len(act) != 2:
				self.request.send(_rERR('wrong command format')) 
				return False
			
			module, action = act
			_log("command: %s action: %s" % (module, action))
			if not modules.module_exists('%s/modules/%s' % (APP_ROOT, module)):
				self.request.send(_rERR('unknown module'))
				return False
			
			mod = modules.load_module(module) 
			
			if hasattr(mod, action):
				method = getattr(mod, action)
				self.request.send(_rOK(method(data))) 
				return True
			else:
				_log("Module does not have %s action" % action)
				self.request.send(_rERR('unknown action'))
				return False
				


args = {
	"host" : "0.0.0.0",
	"port" : "8765",
	"auth" : "%s/.pysock.db" % os.path.expanduser("~"),
}


_next = None
for i in sys.argv[1:]:
	if _next is not None:
		args[_next] = i
		_next = None
		continue
	if i == '-h':
		_next = 'host'
	elif i == '-p':
		_next = 'port'
	elif i == '-f':
		_next = "auth"
	elif i == '-h' or i == '--help':
		_printHelp()
		sys.exit(1)
	
args['port'] = int(args['port'])


if not os.path.isfile(args["auth"]):
	_log("%s does not exists" % args['auth'])
	sys.exit(1)

with open(args["auth"], "r") as auth_file:
	for line in auth_file.readlines():
		line = line.strip().split(':')
		Users.addUser(line[0], line[1], line[2])

server = ThreadedTCPServer((args['host'], args['port']), AuthSocketServer)
ip, port = server.server_address

server_thread = threading.Thread(target=server.serve_forever)

_log("Server startin:\n\tHost: %s\n\tPort: %d" % (args['host'], args['port']))

server_thread.daemon = True
server_thread.run()
