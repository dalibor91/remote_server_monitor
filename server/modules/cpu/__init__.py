import psutil
from server.modules import named_tuple_to_dict as nttd


def times(_):
    return nttd(psutil.cpu_times())


def percent(request):
    return psutil.cpu_percent(percpu=(request == 'percpu'))


def count(request):
    return psutil.cpu_count(logical=(request == 'logical'))


def stats(_):
    return nttd(psutil.cpu_stats())


def freq(request):
    if request == 'percpu':
        return [nttd(cpu) for cpu in psutil.cpu_freq(percpu=True)]
    return nttd(psutil.cpu_freq())


def load(_):
    last1min, last5min, last15min = psutil.getloadavg()
    return {
        'last_1_min': last1min,
        'last_5_min': last5min,
        'last_15_min': last15min
    }
