import json
import time
import base64
import socket
import ConfigParser

#log
def log(message, type="INFO"):
    print "[%s] - %s" % (type, message)

#encoding Server sent events data
def encodeSSE(event, data):
    return "id: %s\ndata: %s\n\n" % (int(time.time()), data)


def read_servers_file(path):
    parser = ConfigParser.ConfigParser();
    parser.read(path)
    data = {}
    for sec in parser.sections():
        data[sec] = {}
        for t in parser.items(sec):
            key, val = t
            data[sec][key] = val

    return data


class SockConnect:
    def __init__(self, data):

        self.host = data['host']
        self.port = int(data['port'])
        self.user = data['user']
        self.pswd = data['pass']
        self.__connect()
        if not self.auth:
            raise Exception("Unable to auth")
        pass


    def __connect(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.auth = False

        self.sock.send('{"command": "auth", "data": { "user":"%s", "pass": "%s" }}' % (self.user, self.pswd))

        resp = json.loads(self.sock.recv(100))
        if 'error' not in resp:
            self.auth = True

    def close(self):
        self.sock.send('{"command": "close"}')
        self.sock.close();


    def pool(self, command):
        self.sock.send('{ "command": "%s" }' % command)
        text = ""
        while 1:
            data = self.sock.recv(1024)
            try:
                data.index("\n")
                text = text+data
                break
            except:
                pass
            text = text+data

        return text
