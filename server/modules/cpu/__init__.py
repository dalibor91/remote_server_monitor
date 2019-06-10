import psutil
from modules import named_tuple_to_dict as nttd

def times(req):
    return nttd(psutil.cpu_times())

def percent(req):
    return psutil.cpu_percent()

"""
def percent_per_cpu(req)
    '''
    interval=1
    if 'interval' in req:
        interval = float(req['interval'])
    '''
    return psutil.cpu_percent(percpu=True)
"""
