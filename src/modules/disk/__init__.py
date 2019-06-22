import psutil
from src.modules import named_tuple_to_dict as nttd


def partitions(_):
    return [nttd(disk) for disk in psutil.disk_partitions()]


def usage(request):
    return nttd(psutil.disk_usage(request))


def io_counters(request):
    if request == 'perdisk':
        _data = psutil.disk_io_counters(perdisk=True)
        data = {}

        for k, v in _data.items():
            data[k] = nttd(v)

        return data
    return nttd(psutil.disk_io_counters())