import unittest
import sys
import os

# add server load packages
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from server.lib import Connection


class TestWithoutConnection(unittest.TestCase):
    def connect(self, *args, **kwargs):
        return Connection(*args, **kwargs)


class TestWithConnection(TestWithoutConnection):
    def setUp(self) -> None:
        self.connection = self.connect("test", "test", host="0.0.0.0")

    def tearDown(self) -> None:
        self.connection.close()
