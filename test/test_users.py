import json
from test import TestWithoutConnection


class TestAuth(TestWithoutConnection):
    def test_user_auth_fail(self) -> None:
        with self.assertRaises(Exception) as e:
            _connection = self.connect("test", "test1", host="0.0.0.0")

        self.assertEqual("Unable to auth %s:%s" % ("test", "test1"), str(e.exception))

    def test_user_success(self) -> None:
        data = None
        with self.connect("test", "test", host="0.0.0.0") as _con:
            data = json.loads(_con.pool("ping.ping"))

        self.assertFalse(data['error'])
        self.assertEqual(data['response'], "pong")

    def test_response(self) -> None:
        with self.connect("test", "test", host="0.0.0.0") as _con:
            self.assertEqual("pong", _con.get('ping.ping').response)

