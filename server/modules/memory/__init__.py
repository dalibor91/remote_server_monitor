import psutil
from server.modules import named_tuple_to_dict as nttd


def virtual(_):
    return nttd(psutil.virtual_memory())


def swap(_):
    return nttd(psutil.swap_memory())