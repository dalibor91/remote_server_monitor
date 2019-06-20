import platform as _platform
from time import time
from socket import gethostname
from socket import gethostbyname
from server.lib.server.auth_server import connections
from server import APP_START


def ping(_):
    return "pong"


def timestamp(_):
    return time()


def hostname(_):
    return gethostname()


def ip(_):
    return gethostbyname(gethostname())


def platform(_):
    return {
        "platform": _platform.platform(),
        "machine": _platform.machine(),
        "processor": _platform.processor(),
        "release": _platform.release(),
        "system": _platform.system(),
        "uname": _platform.uname()
    }


def open_connections(_):
    return connections


def uptime(_):
    return time() - APP_START
