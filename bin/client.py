#!/usr/bin/env python3

import sys
import os
import json

# add server load packages
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from server.lib import Connection

con = Connection("test", "test", host="0.0.0.0")

while True:
    command = input("> ")
    if command == 'quit':
        break

    res = json.loads(con.pool(command), encoding='utf8')

    if res['error']:
        print(">> ERROR: %s" % res['response'])
    else:
        print(">> %s" % res['response'])

con.close()
