import psutil
from .helper import get_proc_info as _proc_info


def all(_):
    return [_proc_info(proc) for proc in psutil.process_iter()]


def pid(id):
    return _proc_info(psutil.Process(int(id)))
