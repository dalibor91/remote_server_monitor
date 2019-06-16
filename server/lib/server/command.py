from ..log import Log
import json


class Command:
    raw_data = None
    obj_data = {}
    error = None
    is_empty = False

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.try_decode()
        self.is_empty = (raw_data == b'')

    def try_decode(self):
        try:
            self.obj_data = json.loads(self.raw_data.decode('utf8'))
            return True
        except Exception as e:
            Log.err(e)
            self.error = e
        return False

    @staticmethod
    def from_request(request):
        try:
            return Command(request.recv(2048).strip())
        except Exception as e:
            Log.err("Command.from_request() -> %s" % str(e))
        return None

    @property
    def command(self):
        if 'command' in self.obj_data:
            return self.obj_data['command']
        return None

    @property
    def data(self):
        if 'data' in self.obj_data:
            return self.obj_data['data']
        return None

    def get(self, name):
        if self.data is not None and name in self.data:
            return self.data[name]
        return None

    def is_command(self, *args):
        for cmd in args:
            if self.command is not None and cmd == self.command:
                return True

        return False



