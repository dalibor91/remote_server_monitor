import socket
import json

class Connection:
    def __init__(self, user, passwd, host="localhost", port=8765):
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

    def close(self):
        self.sock.send('{"command": "close"}')
        self.sock.close()

    def pool(self, command):
        self.sock.send(('{ "command": "%s" }' % command).encode('utf8'))
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
