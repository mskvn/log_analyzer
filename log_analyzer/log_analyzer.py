from .log_analyzer_config import LogAnalyzerConfig
from .log_parser import LogParser
from .log_report import LogReport
from .log_watcher import LogWatcher


def log_analyze():
    config = LogAnalyzerConfig()  # TODO: custom_config_path from --config param
    log = LogWatcher().get_newest_log(config.get_value('LOG_DIR'))
    if not log:
        print('Cant find any suggested log file')  # TODO: logger
        return

    report = LogReport(config.get_value('REPORT_DIR'))
    if report.is_report_exists(log['date']):
        print(f"Newest log is {log['path']}")
        print(f"Report for date {log['date'].strftime('%Y.%m.%d')} already exists")  # TODO: logger, date format
        return

    logs_stats, errors_percent = LogParser().parse_log(log)
    if errors_percent >= config.get_value('MAX_ERROR_PERCENT'):
        print(f"{config.get_value('MAX_ERROR_PERCENT')} % of line did not process")  # TODO: logger

    report_path = report.generate_report(logs_stats, log['date'])
    print(f'See report in {report_path}')


def main():
    try:
        log_analyze()
    except Exception as e:
        print(e)  # TODO: logger


if __name__ == "__main__":
    main()
