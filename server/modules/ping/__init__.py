import platform as _platform
import time
from socket import gethostname
from socket import gethostbyname


def ping(_):
    return "pong"


def timestamp(_):
    return time.time()


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