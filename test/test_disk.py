from test import TestWithConnection


class TestDisk(TestWithConnection):

    partition_fields = ['device', 'fstype', 'opts', 'mountpoint']

    io_counter_fields = [
        'read_time', 'read_merged_count', 'busy_time',
        'read_count', 'write_count', 'write_bytes',
        'read_bytes', 'write_merged_count', 'write_time'
    ]

    def test_partitions(self):
        _partitions = self.get_ok('disk.partitions')
        self.assertIsInstance(_partitions, list)
        self.assertTrue(len(_partitions) > 0)

        for _partition in _partitions:
            for _require in self.partition_fields:
                self.assertIn(_require, _partition)
                self.assertIsInstance(_partition[_require], str)

    def test_usage_fail(self):
        _usage = self.connection.get('disk.usage')
        self.assertTrue(_usage.is_error)

    def test_usage_success(self):
        _usage = self.get_ok('disk.usage', self.get_ok('disk.partitions')[0]['mountpoint'])
        self.assertIsInstance(_usage['percent'], (float, int,))
        self.assertIsInstance(_usage['total'], int)
        self.assertIsInstance(_usage['free'], int)
        self.assertIsInstance(_usage['used'], int)

    def test_io_counters(self):
        _counters = self.get_ok('disk.io_counters')

        for _field in self.io_counter_fields:
            self.assertIn(_field, _counters)
            self.assertIsInstance(_counters[_field], int)

    def test_io_counters_perdisk(self):
        _counters = self.get_ok('disk.io_counters', 'perdisk')

        for _name, _disk in _counters.items():
            self.assertIsInstance(_name, str)
            for _field in self.io_counter_fields:
                self.assertIn(_field, _disk)
                self.assertIsInstance(_disk[_field], int)
