import psutil
from modules import named_tuple_to_dict as nttd

def usage(req):
    return nttd(psutil.virtual_memory())
    
def swap(req):
    return nttd(psutil.swap_memory())
