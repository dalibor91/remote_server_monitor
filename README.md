# SocketServerPy

lightweight monitoring tool in python

server supports multiple clients at once, 
requires authentifications 
and data is exchanged in JSON format

add users 

```bash
bin/users.py add
```

or 

```bash
bin/users.py add -f /path/to/db
```

remove users 
```bash
bin/users.py remove 
```

update users
```bash
bin/users.py update 
```

running server 
```bash
bin/server.py 
```
or 

```bash
bin/server -h localhost -p 9999 -f ./users.txt
```

run tests
```bash 
bin/test
```

host, port, file for auth 
currently users are saved in single text file, but it can be extended to support databases 

connecting to the server 
exaple:
```bash
root@9a0139e2ae76:/server# telnet localhost 8765
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
{"command":"ping.ping","data":"test"}
{"response": "auth", "error": true}
{"command":"auth","data":{"user":"test","pass":"test"}}
{"response": "ok", "error": false}
{"command":"ping.ping"}
{"response": "pong", "error": false}
{"command":"ping.ping"}
{"response": "pong", "error": false}
{"command":"ping.ping"}
{"response": "pong", "error": false}
{"command":"ping.timestamp"}
{"response": 1560706119.0714605, "error": false}
```
