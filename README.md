# Small Monitor

[![Build Status](https://travis-ci.org/dalibor91/pymonitor.svg?branch=master)](https://travis-ci.org/dalibor91/pymonitor)

lightweight monitoring tool with built tcp server, easy to extend with new modules

TCP server requires user auth and all transfered data is in json - utf8 format 

First we need to add users that can use this server 

#### Options 

 - `cpu`
    - `times    `
    - `percent  [percpu]`
    - `count    [logical]`
    - `stats` 
    - `freq     [percpu]`
    - `load` 
 - `disk`
    - `partitions`
    - `usage mount_point`
    - `io_counters [perdisk]`
 - `dummy`
    - `dummy`
    - `error`
 - `memory`
    - `virtual`
    - `swap`
 - `net`
 - `ping`
    - `ping`
    - `hostname`
    - `timestamp`
    - `ip`
    - `uptime`
    - `platform`
  - `process`
    - `all`
    - `pid id`


#### Users 

Adding 
```bash
# add to default user database 
bin/users.py add

# add to specific user database 
bin/users.py add -f /path/to/db 
```

Removing 
```bash
bin/users.py remove 
```

Updating
```bash
bin/users.py update 
```

#### Server
To run server with logs to stdout  
```bash
# -h    - Option for ip address 127.0.0.1
src
src

bin/server.py 
```

To run server as daemon with logs piped to files use service
```bash
bin/service -h localhost -p 9999 -f ./users.txt
```

#### Client 
To start client on server run 
```bash
bin/client
```

example of successful connection 
```bash
root@5950bd5725d0:/server# bin/client
> ping.ping
>> pong
> ping.hostname
>> 5950bd5725d0
> ping.ip
>> 172.17.0.3
> quit
```

#### Tests 

Tests are run inside docker container 
To simple just run tests
```bash 
bin/test
```

run tests and show logs from server 
```bash
bin/test dbg
```


#### Development

For development using docker run 
```bash
bin/docker/build
```

this will build docker image, mount nececary volumes and forward port for you.

all new modules, as current modules are under `server/modules` directory 


#### Example
connecting to the server 
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

#### Installation 

```bash
cd /tmp/
git clone https://github.com/dalibor91/pymonitor.git pymonitor
cd pymonitor
/bin/bash bin/bash/install
```

#### Service 

```bash
# service 
pymomitorctl [start|stop|restart|status]

# user management
pymonitorusr [add|remove|update]

# direct access to server 
pymonitor    [-h host] [-p port] [-f authdb]

# client
pymonitorcli [-h host] [-u user] [-p password]
```
