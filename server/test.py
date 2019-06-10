#!/usr/bin/env python
'''
import modules.server as mserver
import modules.network as mnetwork
import modules.platform as mplatform
import modules.cpu as mcpu

#print mserver.usage(None)
#print mserver.processes(None)
#print mnetwork.interfaces(None)
#print mplatform.current_users(None)
#print mplatform.partitions(None)
#print mplatform.disk_usage_home(None)

#print mcpu.times(None)
print mcpu.percent(None)
'''

import time
import sys
from lib import Connection


con = Connection("test", "test", host="0.0.0.0")

send = sys.argv[1] if len(sys.argv) > 1 else "ping.ping"

while True:
    #print("[%s] S: %s" % (time.time(), send))
    resp = con.pool(send)
    #print("[%s] R: %s" % (time.time(), str(resp).strip()))
    sys.stdout.write("CPU: %s" % str(resp).strip()+"\r");
    sys.stdout.flush()
    time.sleep(0.100)

con.close()



