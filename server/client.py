#!/usr/bin/env python

import socket              
import sys
import json
import time

def _printHelp():
	print(''' 
	Usage 
	./client.py -h <ip> -p <port> -auth user:pass
'''.strip());

data = {
	'host': None,
	'port': None,
	'auth': None
}

_next = None
for i in sys.argv[1:]:
	if _next is not None:
		data[_next] = i
		_next = None
		continue
	if i == '-h':
		_next = 'host'
	elif i == '-p':
		_next = 'port'
	elif i == '-auth':
		_next = 'auth'
	elif i == '-h' or i == '--help':
		_printHelp()
		sys.exit(1)
	
if data['host'] is None or data['port'] is None or data['auth'] is None:
	_printHelp();
	sys.exit(1)


data['port'] = int(data['port'])

user, pwd = data['auth'].split(':', 1)



s = socket.socket()        

s.connect((data['host'], data['port']))

auth = False
poolCommand = None
poolTime = None


while True: 
    try:
	if auth is False:
		s.send(json.dumps({ "command": "auth", "data": { "user":user, "pass": pwd }}))
		try:
			u = json.loads(s.recv(1024))
			if 'error' in u:
				print u['error']
				break
			elif 'response' in u:
				print u['response']
				auth = True
				continue
			else:
				print str(u)
				break
		except Exception, ex:
			print("There is an exception %s" % str(ex))
			continue		

        if poolCommand is None:
            poolCommand = raw_input("Module to pool: ")
            if poolCommand.strip() == "":
                poolCommand = None
                continue
        
        if poolTime is None:
            poolTime = int(raw_input("Seconds to pool: "))
            poolTime = poolTime if poolTime >= 1 else 1


        u = json.dumps({ "command": poolCommand })
        s.send(u)
        print s.recv(1024**2)
        time.sleep(poolTime)

    except Exception, ex:
	print "Exception: %s" % str(ex)
        break
s.close()
