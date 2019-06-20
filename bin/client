#!/usr/bin/env python3

import sys
import os
import json

# add server load packages
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from server.lib import Connection

con = Connection("test", "test", host="0.0.0.0")

while True:
    _command = input("> ")
    if _command == 'quit':
        break

    __command = _command.split(" ", 2)

    data = None
    command = None
    if len(__command) == 2:
        command, data = __command
    else:
        command = __command[0]

    res = json.loads(con.pool(command, data=data), encoding='utf8')

    if res['error']:
        print(">> ERROR: %s" % res['response'])
    else:
        print(">> %s" % res['response'])

con.close()
