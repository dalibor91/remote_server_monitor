from time import time, sleep
from threading import Thread, Lock
from test import TestWithoutConnection


class TestThreadConnections(TestWithoutConnection):
    """
    Run 1000 parralel connections
    """

    thread_processed = 0
    spawn_threads = 1000

    def ping(self, lock: Lock):
        with self.connect("test", "test", host="0.0.0.0") as _con:
            self.assertEqual(_con.get('ping.ping').response, 'pong')
            with lock:
                self.thread_processed += 1

    def test_connections(self):
        _lock = Lock()
        _start = time()
        _queue = []
        for i in range(0, self.spawn_threads):
            _thread = Thread(target=self.ping, args=(_lock,))
            _queue.append(_thread)
            _thread.start()
            _thread.join()

        _runing = True
        while _runing:
            _runing = False
            for thrd in _queue:
                _runing = _runing or thrd.is_alive()

            sleep(1)

        self.assertEqual(self.spawn_threads, self.thread_processed)
        # less than 10 secs
        self.assertTrue((int(time()) - int(_start)) < 10)
