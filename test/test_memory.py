from test import TestWithConnection


class TestMemory(TestWithConnection):
    virtual_memory_fields = [
        'available', 'slab', 'inactive', 'inactive',
        'shared', 'free', 'cached', 'active', 'percent',
        'used', 'buffers', 'total'
    ]

    swap_memory_fields = [
        'percent', 'free', 'sout',
        'used', 'sin', 'total'
    ]

    def test_virtual(self):
        _memory = self.get_ok('memory.virtual')

        for _field in self.virtual_memory_fields:
            if _field == 'percent':
                self.assertIsInstance(_memory[_field], (float, int,))
            else:
                self.assertIsInstance(_memory[_field], int)

    def test_swap(self):
        _memory = self.get_ok('memory.swap')

        for _field in self.swap_memory_fields:
            if _field == 'percent':
                self.assertIsInstance(_memory[_field], (float, int,))
            else:
                self.assertIsInstance(_memory[_field], int)
