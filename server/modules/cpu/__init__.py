import psutil
from server.modules import named_tuple_to_dict as nttd


def times(request):
    return nttd(psutil.cpu_times())


def percent(request):
    return psutil.cpu_percent()

