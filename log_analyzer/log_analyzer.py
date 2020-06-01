import sys

from .log_analyzer_config import LogAnalyzerConfig
from .log_parser import LogParser
from .log_watcher import LogWatcher


def generate_report(logs_stats, logs_date):
    pass


def main():
    config = LogAnalyzerConfig()
    log = LogWatcher.get_newest_log(config.get_value('LOG_DIR'))
    if not log:
        print('Cant find any suggested log file')  # TODO: logger
        sys.exit(0)
    logs_stats = LogParser.parse_log()
    generate_report(logs_stats, log['date'])


if __name__ == "__main__":
    main()
