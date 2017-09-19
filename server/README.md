# SocketServerPy
test python socket server with auth

server supports multiple clients at once, 
requires authentifications 
and data is exchanged in JSON format

add users 
```
./users.py add
```

or 

```
./users.py add -f /path/to/db
```

remove users 
```
users.py remove 
```

update users
```
users.py update 
```

running server 
```
server.py 
```
or 

```
server -h localhost -p 9999 -f ./users.txt
```
host, port, file for auth 
currently users are saved in single text file, but it can be extended to support databases 

connecting to the server 
exaple:
```
dalibor@vg$ nc localhost 9999
{"command":"ping.ping","data":"test"}
{"error": "Please auth"}
{"command":"auth","data":{"user":"test","pass":"test"}}
{"response": "Hello test"}
{"command":"ping.ping"}}
{"response": "pong"}
{"command":"ping.ping"}}
{"response": "pong"}
{"command":"ping.ping"}}
{"response": "pong"}
{"command":"close"}
```
