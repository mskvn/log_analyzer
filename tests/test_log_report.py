import json
import os
import unittest
from datetime import datetime

from log_analyzer.log_report import LogReport


class TestLogParser(unittest.TestCase):

    def test_generate_report(self):
        report_path = os.path.join('fixtures', 'tmp')
        report = LogReport(report_path)
        logs_date = datetime.strptime('2020.01.02', '%Y.%m.%d')
        with open(os.path.join('fixtures', 'logs_stats.json')) as f:
            logs_stats = json.loads(f.read())
        report.generate_report(logs_stats, logs_date)

        self.assertTrue(os.path.isfile(os.path.join(report_path, 'report-2020.01.02.html')))

    def test_is_report_exists(self):
        report = LogReport('fixtures/reports')
        logs_date = datetime.strptime('2020.01.01', '%Y.%m.%d')
        self.assertTrue(report.is_report_exists(logs_date))
