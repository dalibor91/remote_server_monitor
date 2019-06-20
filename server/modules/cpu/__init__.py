import psutil
from typing import Dict, Union
from server.modules import named_tuple_to_dict as nttd


def times(_) -> Dict:
    return nttd(psutil.cpu_times())


def percent(request: Union[str, Dict]) -> Union[int, float, Dict]:
    return psutil.cpu_percent(percpu=(request == 'percpu'))


def count(request: Union[str, Dict]) -> int:
    return psutil.cpu_count(logical=(request == 'logical'))


def stats(_) -> Dict:
    return nttd(psutil.cpu_stats())


def freq(request: Union[str, Dict]) -> Union[Dict, list]:
    if request == 'percpu':
        return [nttd(cpu) for cpu in psutil.cpu_freq(percpu=True)]
    return nttd(psutil.cpu_freq())


def load(_) -> Dict:
    last1min, last5min, last15min = psutil.getloadavg()
    return {
        'last_1_min': last1min,
        'last_5_min': last5min,
        'last_15_min': last15min
    }
