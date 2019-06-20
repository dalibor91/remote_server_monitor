from test import TestWithConnection


class TestCpu(TestWithConnection):
    def test_percentage(self) -> None:
        res = self.get_ok('cpu.percent')
        self.assertTrue(isinstance(res, float) or isinstance(res, int))

    def test_percentage_per_core(self) -> None:
        res = self.get_ok('cpu.percent', 'percpu')
        self.assertTrue(isinstance(res, list))
        for usage_percentage in res:
            self.assertTrue(isinstance(usage_percentage, float) or isinstance(usage_percentage, int))

    def test_count(self) -> None:
        res = self.get_ok('cpu.count')
        self.assertTrue(isinstance(res, int))
        self.assertTrue(res > 0)

    def test_count_logical(self) -> None:
        res = self.get_ok('cpu.count', 'logical')
        self.assertTrue(isinstance(res, int))
        self.assertTrue(res > 0)

    def test_freq(self) -> None:
        res = self.get_ok('cpu.freq')
        self.assertTrue('min' in res)
        self.assertTrue('current' in res)
        self.assertTrue('max' in res)

        self.assertTrue(isinstance(res['min'], float) or isinstance(res['min'], int))
        self.assertTrue(isinstance(res['max'], float) or isinstance(res['max'], int))
        self.assertTrue(isinstance(res['current'], float) or isinstance(res['current'], int))

    def test_freq_percpu(self) -> None:
        res = self.get_ok('cpu.freq', 'percpu')
        self.assertEqual(self.get_ok('cpu.count', 'logical'), len(res))

        for cpu_data in res:
            self.assertTrue('min' in cpu_data)
            self.assertTrue('max' in cpu_data)
            self.assertTrue('current' in cpu_data)

            self.assertTrue(
                isinstance(cpu_data['min'], float) or isinstance(cpu_data['min'], int))
            self.assertTrue(
                isinstance(cpu_data['max'], float) or isinstance(cpu_data['max'], int))
            self.assertTrue(
                isinstance(cpu_data['current'], float) or isinstance(cpu_data['current'], int))

    def test_load(self) -> None:
        res = self.get_ok('cpu.load')

        self.assertTrue('last_1_min' in res)
        self.assertTrue('last_5_min' in res)
        self.assertTrue('last_15_min' in res)

        self.assertTrue(
            isinstance(res['last_1_min'], float) or isinstance(res['last_1_min'], int))
        self.assertTrue(
            isinstance(res['last_5_min'], float) or isinstance(res['last_5_min'], int))
        self.assertTrue(
            isinstance(res['last_15_min'], float) or isinstance(res['last_15_min'], int))
