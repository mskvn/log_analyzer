import json
import os
import unittest
from datetime import datetime

from log_analyzer.log_report import LogReport


class TestLogParser(unittest.TestCase):
    _fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

    def test_generate_report(self):
        report = LogReport(report_dir=os.path.join(self._fixtures, 'tmp'))
        logs_date = datetime.strptime('2020.01.02', '%Y.%m.%d')
        with open(os.path.join(self._fixtures, 'logs_stats.json')) as f:
            logs_stats = json.loads(f.read())
        report_path = report.generate_report(logs_stats, logs_date, 3)

        self.assertTrue(os.path.isfile(report_path))

    def test_is_report_exists(self):
        report = LogReport(report_dir=os.path.join(self._fixtures, 'reports'))
        logs_date = datetime.strptime('2020.01.01', '%Y.%m.%d')
        self.assertTrue(report.is_report_exists(logs_date))
