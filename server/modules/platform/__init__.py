import platform
import psutil
import datetime
from modules import named_tuple_to_dict as nttd

def info(req):
    return {
        "machine_type": platform.machine(),
        "network_name": platform.node(),
        "processor": platform.processor(),
        "system_release": platform.release(),
        "system": platform.system(),
        "system_version": platform.version(),
        "bootime": psutil.boot_time(),
        "boottime_formated": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    }


def current_users(req):
    data = []
    for usr in psutil.users():
        data.append({
            "username": usr.name,
            "terminal": usr.terminal,
            "host": usr.host,
            "started": usr.started,
            "started_formated" : datetime.datetime.fromtimestamp(usr.started).strftime("%Y-%m-%d %H:%M:%S")
        })

    return data

def partitions(req):
    data = []
    for i in psutil.disk_partitions():
        data.append(nttd(i))

    return data

def _disk_usage(req, l):
    return nttd(psutil.disk_usage(l))

def disk_usage_root(req):
    return _disk_usage(req, '/')

def disk_usage_home(req):
    return _disk_usage(req, '/home')
