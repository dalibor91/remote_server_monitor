from datetime import datetime
from sys import stdout
from sys import stderr


def _log(msg: str) -> None:
    stdout.write(msg)
    stdout.flush()


def _err(msg: str) -> None:
    stderr.write(msg)
    stderr.flush()


class Log():
    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod 
    def log(msg: str) -> None:
        _log("LOG %s : %s\n" % (Log.timestamp(), str(msg)))

    @staticmethod
    def err(msg: str) -> None:
        _err("ERR %s : %s\n" % (Log.timestamp(), str(msg)))

