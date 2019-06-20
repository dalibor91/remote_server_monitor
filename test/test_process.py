from test import TestWithConnection


class TestMemory(TestWithConnection):

    fields = {
        'name': str,
        'cwd': str,
        'cpu_percent': float,
        'username': str,
        'terminal': str,
        'status': str,
        'cmd_line': list,
        'exe': str,
        'threads': int,
        'ppid': int,
        'create_time': float,
        'pid': int
    }

    def test_all_processes(self):
        for _process in self.get_ok('process.all'):
            for _name, _val in _process.items():
                if _name == 'terminal':
                    self.assertTrue(_val is None or isinstance(_val, str))
                else:
                    self.assertIsInstance(_val, self.fields[_name])

    def test_pid(self):
        _pid = self.get_ok('process.all')[0]['pid']

        for _name, _val in self.get_ok('process.pid', _pid).items():
            if _name == 'terminal':
                self.assertTrue(_val is None or isinstance(_val, str))
            else:
                self.assertIsInstance(_val, self.fields[_name])