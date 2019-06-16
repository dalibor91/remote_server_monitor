from datetime import datetime
from sys import stdout
from sys import stderr


def _log(msg):
    stdout.write(msg)
    stdout.flush()


def _err(msg):
    stderr.write(msg)
    stderr.flush()


class Log():
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod 
    def log(msg):
        _log("LOG %s : %s\n" % (Log.timestamp(), str(msg)))

    @staticmethod
    def err(msg):
        _err("ERR %s : %s\n" % (Log.timestamp(), str(msg)))

