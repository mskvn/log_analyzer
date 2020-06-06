import os
import re
from datetime import datetime


class LogWatcher:
    LOG_FILE_REGEXP = r"nginx-access-ui\.log-(?P<date>[0-9]{8})($|\.(?P<ext>gz)$)"
    DATE_FORMAT = '%Y%m%d'

    def get_newest_log(self, log_dir):
        """
        Scan log_dir, find file with names like LOG_FILE_REGEXP, and return the newest one
        :param log_dir: directory where log file should be find
        :return: dict
        Returned dict contains few keys: path, date and ext
        """
        return max(self._suitable_logs(log_dir), key=lambda x: x['date'], default=None)

    def _suitable_logs(self, log_dir):
        files = os.listdir(log_dir)
        for log_path in files:
            match = re.search(self.LOG_FILE_REGEXP, log_path)
            if match:
                log_date = datetime.strptime(match.group('date'), self.DATE_FORMAT)
                yield {'path': os.path.join(log_dir, log_path), 'date': log_date, 'ext': match.group('ext')}
