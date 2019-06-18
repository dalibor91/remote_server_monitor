from test import TestWithConnection
from time import time
from socket import gethostname
from socket import gethostbyname


class TestPing(TestWithConnection):
    def test_pong(self) -> None:
        self.assertEqual('pong', self.connection.get('ping.ping').response)

    def test_timestamp(self) -> None:
        self.assertAlmostEqual(self.connection.get('ping.timestamp').response, time(), delta=0.5)

    def test_hostname(self) -> None:
        self.assertEqual(gethostname(), self.connection.get('ping.hostname').response)

    def test_ip(self) -> None:
        self.assertEqual(gethostbyname(gethostname()), self.connection.get('ping.ip').response)

    def test_platform(self) -> None:
        has_values = [
            "platform", "machine", "processor",
            "release", "system", "uname"
        ]

        resp = self.connection.get('ping.platform').response

        for val in has_values:
            self.assertTrue(val in resp)
            self.assertTrue(isinstance(resp[val], (str, list,)))

    def test_open_connections(self) -> None:
        _cons = self.connection.get('ping.open_connections').response
        _ip, _port = self.connection.sock.getsockname()

        self.assertEqual({ "%s:%s" % (_ip, _port) : 1 }, _cons)

    def test_uptime(self) -> None:
        _uptime = self.connection.get('ping.uptime').response
        self.assertTrue(isinstance(_uptime, float))
