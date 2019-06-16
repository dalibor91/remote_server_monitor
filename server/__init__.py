'''
Defining default configuration
For server
'''

from os import path
from .lib import argv

APP_ROOT = path.dirname(path.dirname(path.realpath(__file__)))
APP_HOST = argv.get('h', default='0.0.0.0')
APP_PORT = int(argv.get('p', default=8765))
APP_AUTH_DB = argv.get('f', default="%s/.srvmonitor.db" % path.expanduser("~"))


