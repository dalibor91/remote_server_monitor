import socket
import json
from typing import Union, Dict

class Response:
    def __init__(self, response):
        self._response = json.loads(response)

    @property
    def is_error(self) -> bool:
        return 'error' in self._response and self._response['error']

    @property
    def response(self) -> Union[None, Dict, str]:
        return self._response['response']


class Connection:
    def __init__(self, user: str, passwd: str, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = int(port)
        self.user = user
        self.pswd = passwd
        self.__connect()

        if not self.auth:
            raise Exception("Unable to auth %s:%s" % (self.user, self.pswd))

    def __connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.auth = False

        self.sock.send(('{"command": "auth", "data": { "user":"%s", "pass": "%s" }}' % (self.user, self.pswd)).encode('utf8'))
        resp = json.loads(self.sock.recv(100).decode('utf-8'))
        if 'error' in resp and not resp['error']:
            self.auth = True
        else:
            self.sock.close()
            self.sock = None

    def close(self):
        if self.sock:
            self.sock.send('{"command": "close"}'.encode('utf8'))
            self.sock.close()

    def pool(self, command: str, data: Union[None, str] = None):
        self.sock.send(('{ "command": "%s", "data": "%s" }' % (command, "" if data is None else str(data))).encode('utf8'))
        text = ""
        while 1:
            data = self.sock.recv(1024).decode('utf8')
            try:
                data.index("\n")
                text = text+data
                break
            except:
                pass
            text = text+data

        return text

    def get(self, command: str, data: Union[None, str] = None):
        return Response(self.pool(command, data=data))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
