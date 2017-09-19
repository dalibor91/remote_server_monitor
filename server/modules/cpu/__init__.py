import psutil
from modules import named_tuple_to_dict as nttd

def times(req):
    return nttd(psutil.cpu_times())

def percent(req):
    return psutil.cpu_percent()
