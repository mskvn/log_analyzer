import os
import unittest
import unittest.mock as mock

from log_analyzer.log_watcher import LogWatcher


class TestLogWatcher(unittest.TestCase):

    def test_get_newest_log(self):
        logs = ['nginx-access-ui.log-20170630', 'nginx-access-ui.log-20170629']
        log_dir = '/some/path/'
        log = self.__get_newest_logs_with_mock(log_dir, logs)
        self.assertEqual(log['path'], os.path.join(log_dir, logs[0]))

    def test_get_newest_log_only_plain_and_gz(self):
        logs = ['nginx-access-ui.log-20170630.bz2', 'nginx-access-ui.log-20170629.gz']
        log_dir = '/some/path/'
        log = self.__get_newest_logs_with_mock(log_dir, logs)
        self.assertEqual(log['path'], os.path.join(log_dir, logs[1]))

    def test_get_newest_log_not_suitable(self):
        logs = ['nginx-access-ui.log-20170630.bz2', 'nginx-access-ui.log-20170629.txt']
        log_dir = '/some/path/'
        log = self.__get_newest_logs_with_mock(log_dir, logs)
        self.assertIsNone(log)

    def test_get_newest_log_ext(self):
        logs = ['nginx-access-ui.log-20170630.gz']
        log_dir = '/some/path/'
        log = self.__get_newest_logs_with_mock(log_dir, logs)
        self.assertEqual(log['ext'], 'gz')

    @staticmethod
    def __get_newest_logs_with_mock(log_dir, mocked_logs):
        with mock.patch('os.listdir') as log_dir_listdir:
            log_dir_listdir.return_value = mocked_logs
            return LogWatcher().get_newest_log(log_dir)
