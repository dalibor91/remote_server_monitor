from test import TestWithConnection


class TestCpu(TestWithConnection):
    def test_percentage(self) -> None:
        res = self.connection.get('cpu.percent')
        self.assertTrue(isinstance(res.response, float) or isinstance(res.response, int))

    def test_percentage_per_core(self) -> None:
        res = self.connection.get('cpu.percent', 'percpu')
        self.assertTrue(isinstance(res.response, list))
        for usage_percentage in res.response:
            self.assertTrue(isinstance(usage_percentage, float) or isinstance(usage_percentage, int))

    def test_count(self) -> None:
        res = self.connection.get('cpu.count')
        self.assertTrue(isinstance(res.response, int))
        self.assertTrue(res.response > 0)

    def test_count_logical(self) -> None:
        res = self.connection.get('cpu.count', 'logical')
        self.assertTrue(isinstance(res.response, int))
        self.assertTrue(res.response > 0)

    def test_freq(self) -> None:
        res = self.connection.get('cpu.freq')
        self.assertTrue('min' in res.response)
        self.assertTrue('current' in res.response)
        self.assertTrue('max' in res.response)

        self.assertTrue(isinstance(res.response['min'], float) or isinstance(res.response['min'], int))
        self.assertTrue(isinstance(res.response['max'], float) or isinstance(res.response['max'], int))
        self.assertTrue(isinstance(res.response['current'], float) or isinstance(res.response['current'], int))

    def test_freq_percpu(self) -> None:
        res = self.connection.get('cpu.freq', 'percpu')
        self.assertEqual(self.connection.get('cpu.count', 'logical').response, len(res.response))

        for cpu_data in res.response:
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
        res = self.connection.get('cpu.load')

        self.assertTrue('last_1_min' in res.response)
        self.assertTrue('last_5_min' in res.response)
        self.assertTrue('last_15_min' in res.response)

        self.assertTrue(
            isinstance(res.response['last_1_min'], float) or isinstance(res.response['last_1_min'], int))
        self.assertTrue(
            isinstance(res.response['last_5_min'], float) or isinstance(res.response['last_5_min'], int))
        self.assertTrue(
            isinstance(res.response['last_15_min'], float) or isinstance(res.response['last_15_min'], int))
