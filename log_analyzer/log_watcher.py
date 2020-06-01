import os
import re
from datetime import datetime


class LogWatcher:
    LOG_FILE_REGEXP = r"nginx-access-ui\.log-(?P<date>[0-9]{8})($|\.(?P<ext>gz)$)"
    DATE_FORMAT = '%Y%m%d'

    def get_newest_log(self, log_dir):
        return max(self.__suitable_logs(log_dir), key=lambda x: x['date'], default=None)

    def __suitable_logs(self, log_dir):
        files = os.listdir(log_dir)
        for log_path in files:
            match = re.search(self.LOG_FILE_REGEXP, log_path)
            if match:
                log_date = datetime.strptime(match.group('date'), self.DATE_FORMAT)
                yield {'path': os.path.join(log_dir, log_path), 'date': log_date, 'ext': match.group('ext')}
