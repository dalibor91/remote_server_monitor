import psutil
from modules import named_tuple_to_dict as nttd

def processes(d):
    data = []

    for proc in psutil.process_iter():
        m = {
            "name": proc.name(),
            "username": proc.username(),
            "ppid" : proc.ppid(),
            "pid": proc.pid,
            "status": proc.status(),
            "create_time": proc.create_time(),
            "terminal": proc.terminal(),
            #"threads": proc.num_threads(),
            "cmd_line": proc.cmdline(),
            #"exe": proc.exe(),
            #"cwd": proc.cwd(),
            "cpu_percent": proc.cpu_percent()
        }

        #special permissions
        try :
            m["threads"] = proc.num_threads()
            #m["cmd_line"] = proc.cmd_line(),
            m["cwd"] = proc.cwd();
            m["exe"] = proc.exe();
            for k,v in nttd(proc.memory_full_info()):
                m["memory_%s" % k] = v
        except:
            pass

        data.append(m)

    return data
    
    
def info(req):
    from modules import cpu as mcpu
    from modules import ram as mram 
    from modules import platform as mplatform
    
    return {
        "cpu_percent": mcpu.percent(req),
        "cpu_times": mcpu.times(req),
        "ram": mram.usage(req), 
        "swap": mram.swap(req), 
        "usage_home": mplatform.disk_usage_home(req),
        "usage_root": mplatform.disk_usage_root(req)
    }
    
    



def __disk_io_counters(d):
    n_c = psutil.disk_io_counters()
    data = {}
    for tpl in n_c._asdict().items():
        k,v = tpl
        data[k] = v

    return data

#done
def __cpu_times(d):
    n_c = psutil.cpu_times()
    data = {}
    for tpl in n_c._asdict().items():
        k,v = tpl
        data[k] = v

    return data

#done
def __cpu_percent(d):
    return psutil.cpu_percent()

def __virtual_memory(d):
    n_c = psutil.virtual_memory()
    data = {}
    for tpl in n_c._asdict().items():
        k,v = tpl
        data[k] = v

    return data

def __swap_memory(d):
    n_c = psutil.swap_memory()
    data = {}
    for tpl in n_c._asdict().items():
        k,v = tpl
        data[k] = v

    return data


def usage(d):
    return {
        "disk_counters": __disk_io_counters(d),
        "cpu_times": __cpu_times(d),
        "cpu_percent": __cpu_percent(d),
        "virtual_memory": __virtual_memory(d),
        "swap_memory": __swap_memory(d)
    }
    #return network_usage
