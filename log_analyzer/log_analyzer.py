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
        print(f"Report for date {log['date'].strftime('%Y.%m.%d')} already exists")  # TODO: logger
        return

    logs_stats = LogParser().parse_log(log, config.get_value('MAX_ERROR_PERCENT'))

    if len(logs_stats) == 0:
        print('Don`t have enough data for generate report')  # TODO: logger, warn
        return

    print('Generating report')  # TODO: logger
    report_path = report.generate_report(logs_stats, log['date'], int(config.get_value('REPORT_SIZE')))
    print(f'See report in {report_path}')  # TODO: logger, info
