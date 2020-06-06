import os
import unittest

from log_analyzer.log_parser import LogParser


class TestLogParser(unittest.TestCase):

    def test_parse_log(self):
        log_plain = {
            'path': os.path.join('fixtures', 'logs', 'nginx-log'),
            'ext': ''
        }
        log_gz = {
            'path': os.path.join('fixtures', 'logs', 'nginx-log.gz'),
            'ext': 'gz'
        }
        for log in [log_plain, log_gz]:
            with self.subTest(log=log):
                report_stat = LogParser().parse_log(log, 0.1)
                self.assertIsInstance(report_stat, list)
                url_stat = report_stat[0]
                required_keys = ['url', 'count', 'count_perc', 'time_avg', 'time_med', 'time_max', 'time_sum',
                                 'time_perc']
                for key in required_keys:
                    self.assertTrue(key in url_stat, f'Key {key} absence in url stats')
                self.assertEqual(len(report_stat), 10)
