import json
import os
import string


class LogReport:
    REPORT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates', 'report.html')
    REPORT_NAME_FORMAT = 'report-%Y.%m.%d.html'

    def __init__(self, report_dir):
        self._report_dir = report_dir

    def generate_report(self, logs_stats, logs_date, report_size):
        if len(logs_stats) > report_size:
            logs_stats = logs_stats[0:report_size]
        logs_stats = sorted(logs_stats, key=lambda x: x['time_sum'])

        with open(self.REPORT_TEMPLATE_PATH, encoding="ascii", errors="surrogateescape", mode='r') as f:
            template = string.Template(f.read())
        with open(self._report_path(logs_date), 'w+') as f:
            f.write(template.safe_substitute(table_json=json.dumps(logs_stats)))

        return self._report_path(logs_date)

    def is_report_exists(self, logs_date):
        return os.path.isfile(self._report_path(logs_date))

    def _report_path(self, logs_date):
        return os.path.join(self._report_dir, logs_date.strftime(self.REPORT_NAME_FORMAT))
