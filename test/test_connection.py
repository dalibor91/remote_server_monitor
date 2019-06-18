from test import TestWithoutConnection
from time import sleep

class TestConnection(TestWithoutConnection):
    def test_quit(self):
        con1 = self.connect("test", "test", host="0.0.0.0")
        con2 = self.connect("test", "test", host="0.0.0.0")
        con3 = self.connect("test", "test", host="0.0.0.0")

        con1.sock.send(b'{"command": "quit", "data": ""}')
        con2.sock.send(b'{"command": "exit", "data": ""}')
        con3.sock.send(b'{"command": "close", "data": ""}')

        with self.assertRaises(Exception) as e:
            data = json.loads(con1.sock.recv(1024).decode('utf8').strip())
            self.assertEqual(data['response'], 'quit')
            con1.sock.send(b'{"command": "quit", "data": ""}')
            self.assertEqual("", con1.sock.recv(200))


        with self.assertRaises(Exception) as e:
            data = json.loads(con2.sock.recv(1024).decode('utf8').strip())
            self.assertEqual(data['response'], 'quit')
            con1.sock.send(b'{"command": "quit", "data": ""}')
            self.assertEqual("", con2.sock.recv(200))

        with self.assertRaises(Exception) as e:
            data = json.loads(con3.sock.recv(1024).decode('utf8').strip())
            self.assertEqual(data['response'], 'quit')
            con1.sock.send(b'{"command": "quit", "data": ""}')
            self.assertEqual("", con3.sock.recv(200))

        con1.sock.close()
        con2.sock.close()
        con3.sock.close()

    def test_multiple_connections(self):
        _cons = range(0, 100)
        _opened = {}

        main_connection = self.connect("test", "test", host="0.0.0.0")

        for _conid in _cons:
            _opened[_conid] = self.connect("test", "test", host="0.0.0.0")

        self.assertEqual(len(main_connection.get('ping.open_connections').response), len(_cons)+1)

        for _conid in range(50, 100):
            _opened[_conid].close()
            del _opened[_conid]

        # wait to be removed
        sleep(1)

        self.assertEqual(len(main_connection.get('ping.open_connections').response), len(_opened) + 1)

        for _, _con in _opened.items():
            _con.close()

        # wait for rest to be removed
        sleep(1)

        self.assertEqual(len(main_connection.get('ping.open_connections').response), 1)

        main_connection.close()
