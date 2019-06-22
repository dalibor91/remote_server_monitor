from src.modules import named_tuple_to_dict as nttd


def get_proc_info(proc):
    m = {
        "name": proc.name(),
        "username": proc.username(),
        "ppid": proc.ppid(),
        "pid": proc.pid,
        "status": proc.status(),
        "create_time": proc.create_time(),
        "terminal": proc.terminal(),
        "cmd_line": proc.cmdline(),
        "cpu_percent": proc.cpu_percent()
    }

    # special permissions
    try:
        m["threads"] = proc.num_threads()
        # m["cmd_line"] = proc.cmd_line(),
        m["cwd"] = proc.cwd();
        m["exe"] = proc.exe();
        for k, v in nttd(proc.memory_full_info()):
            m["memory_%s" % k] = v
    except:
        pass

    return m