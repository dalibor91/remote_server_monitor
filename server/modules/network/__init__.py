import psutil
import socket
from modules import named_tuple_to_dict as nttd

def io_counters(req):
    return nttd(psutil.net_io_counters())


def connections(req):
    data = []
    try:
        cons = psutil.net_connections()
        for con in cons:
            data.append({
                "local_address": con.laddr.ip,
                "local_port": con.laddr.port,
                "remote_address": con.raddr.ip if len(con.raddr) > 0 else None,
                "remote_port": con.raddr.port if len(con.raddr) > 0 else None,
                "status": con.status,
                "pid": con.pid,
                "family": con.family
            })
    except Exception, e:
        print e
        pass

    return data

def interfaces(req):

    data = []
    for name, t in psutil.net_if_addrs().items():
        for i in t:
            data.append({
                "name" : name,
                "address": i.address,
                "netmask": i.netmask,
                "broadcast": i.broadcast
            })

    return data
