from test import TestWithConnection
from time import time
from socket import gethostname
from socket import gethostbyname


class TestPing(TestWithConnection):
    def test_pong(self) -> None:
        self.assertEqual('pong', self.get_ok('ping.ping'))

    def test_timestamp(self) -> None:
        self.assertAlmostEqual(self.get_ok('ping.timestamp'), time(), delta=0.5)

    def test_hostname(self) -> None:
        self.assertEqual(gethostname(), self.get_ok('ping.hostname'))

    def test_ip(self) -> None:
        self.assertEqual(gethostbyname(gethostname()), self.get_ok('ping.ip'))

    def test_platform(self) -> None:
        has_values = [
            "platform", "machine", "processor",
            "release", "system", "uname"
        ]

        resp = self.get_ok('ping.platform')

        for val in has_values:
            self.assertTrue(val in resp)
            self.assertTrue(isinstance(resp[val], (str, list,)))

    def test_open_connections(self) -> None:
        _cons = self.get_ok('ping.open_connections')
        _ip, _port = self.connection.sock.getsockname()

        self.assertEqual({ "%s:%s" % (_ip, _port) : 1 }, _cons)

    def test_uptime(self) -> None:
        _uptime = self.get_ok('ping.uptime')
        self.assertTrue(isinstance(_uptime, float))
