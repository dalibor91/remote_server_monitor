from ..log import Log
from .command import Command
from .response import Response
from .user import Users
from socketserver import BaseRequestHandler
from hashlib import sha224
import importlib


def load_module(name):
    return importlib.import_module("server.modules.%s" % name)


class AuthServer(BaseRequestHandler):
    @property
    def _get_str(self):
        return str({
            "auth": self.auth,
            "auth_no": self.auth_no,
            "loop": self.loop,
        })

    def _on_fail_response(self, e):
        self.loop = False
        Log.err("Failed sending response AuthServer._on_fail_response")
        Log.err(e)

    def _initialize(self):
        ''' Initializes server '''
        self.auth = False
        self.auth_no = 0
        self.loop = True
        self.res = Response(self.request, self._on_fail_response)
        Log.log("Initialize AuthServer._initialize()")

    def _authorize(self, cmd):
        ''' Authorizes user '''
        self.auth_no += 1

        if self.auth_no >= 3:
            self.loop = False
            return

        _user = cmd.get('user')
        _pass = cmd.get('pass')
        if _user is None or _pass is None:
            self.auth = False
        else:
            user = Users.user(_user)
            if user is not None:
                self.auth = (sha224(_pass.encode('utf8')).hexdigest() == user['password'])

        if self.auth:
            self.res.ok('ok')
            self.auth_no = 0
        else:
            self.res.err('auth fail')

        Log.log("Initialize AuthServer._authorize(%s)" % self._get_str)

    def _handle_cmd(self, cmd):
        Log.log("AuthServer._handle_cmd(%s)" % str(cmd))
        if cmd.command:
            _data = cmd.command.rsplit('.', 1)

            if len(_data) == 2:
                _module, _command = _data

                try:
                    module = load_module(_module)

                    if hasattr(module, _command):
                        method = getattr(module, _command)
                        try:
                            self.res.ok(method(cmd.data))
                        except Exception as ex:
                            self.res.err('Calling method "%s" resulted in error' % _command)
                    else:
                        self.res.err('command "%s" does not exists' % str(_command))
                except Exception as e:
                    Log.err(e)
                    self.res.err('module "%s" not found' % str(_module))
            else:
                self.res.err('command should have 2 parts')
        else:
            self.res.err('command not found')

    def handle(self):
        self._initialize()

        while self.loop:
            cmd = Command.from_request(self.request)
            if cmd.is_empty:
                self.res.ok('quit_empty')
                break

            if cmd is None or cmd.error is not None:
                self.res.err("error: %s" % "unable to process command" if cmd is None else str(cmd.error))
                break

            if cmd.is_command('quit', 'close', 'exit'):
                self.res.ok("quit")
                break

            if cmd.is_command('login', 'auth'):
                self._authorize(cmd)
            elif self.auth:
                self._handle_cmd(cmd)
            else:
                self.res.err("auth")
