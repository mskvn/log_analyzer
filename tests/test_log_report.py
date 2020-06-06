import json
import os
import unittest
from datetime import datetime

from log_analyzer.log_report import LogReport


class TestLogParser(unittest.TestCase):

    def test_generate_report(self):
        report_dir = os.path.join('fixtures', 'tmp')
        report = LogReport(report_dir)
        logs_date = datetime.strptime('2020.01.02', '%Y.%m.%d')
        with open(os.path.join('fixtures', 'logs_stats.json')) as f:
            logs_stats = json.loads(f.read())
        report_path = report.generate_report(logs_stats, logs_date, 3)

        self.assertTrue(os.path.isfile(report_path))

    def test_is_report_exists(self):
        report = LogReport('fixtures/reports')
        logs_date = datetime.strptime('2020.01.01', '%Y.%m.%d')
        self.assertTrue(report.is_report_exists(logs_date))
