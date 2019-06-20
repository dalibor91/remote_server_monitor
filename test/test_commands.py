import json
from test import TestWithConnection


class TestCommand(TestWithConnection):
    def test_command_not_valid(self) -> None:
        res = self.connection.get('test')
        self.assertTrue(res.is_error)
        self.assertEqual("command should have 2 parts", res.response)

    def test_module_not_found(self) -> None:
        res = self.connection.get('test.test')
        self.assertTrue(res.is_error)
        self.assertEqual('module "test" not found', res.response)

    def test_command_not_found(self) -> None:
        res = self.connection.get('dummy.asdferge')
        self.assertTrue(res.is_error)
        self.assertEqual('command "asdferge" does not exists', res.response)

    def test_command_error(self):
        res = self.connection.get('dummy.error')
        self.assertTrue(res.is_error)
        self.assertEqual('Calling method "error" resulted in error', res.response)

    def test_command_ok(self):
        res = self.connection.get('dummy.dummy')
        self.assertFalse(res.is_error)
        self.assertEqual('dummy', res.response)

    def test_command_not_sent(self):
        self.connection.sock.send('{"data": "test"}'.encode('utf8'))
        data = json.loads(self.connection.sock.recv(1024).decode('utf8').strip())
        self.assertEqual(data['response'], 'command not found')
        self.assertTrue(data['error'])
