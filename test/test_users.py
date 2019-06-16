import unittest
import sys
import os
import json

# add server load packages
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from server.lib import Connection

class TestAuth(unittest.TestCase):
    def test_user_auth_fail(self):
        with self.assertRaises(Exception) as e:
            _connection = Connection("test", "test1", host="0.0.0.0")
            _connection.close()

        self.assertEqual("Unable to auth %s:%s" % ("test", "test1"), str(e.exception))

    def test_user_success(self):
        data = None
        with Connection("test", "test", host="0.0.0.0") as _con:
            data = json.loads(_con.pool("ping.ping"))

        self.assertFalse(data['error'])
        self.assertEqual(data['response'], "pong")

