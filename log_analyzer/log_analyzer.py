import logging

from .log_parser import LogParser
from .log_report import LogReport
from .log_watcher import LogWatcher


def log_analyze(config):
    log = LogWatcher().get_newest_log(config.get_value('LOG_DIR'))
    if not log:
        logging.info('Cant find any suggested log file')
        return

    report = LogReport(config.get_value('REPORT_DIR'))
    if report.is_report_exists(log['date']):
        logging.info(f"Newest log is {log['path']}")
        logging.info(f"Report for date {log['date'].strftime('%Y.%m.%d')} already exists")
        return

    logs_stats = LogParser().parse_log(log, config.get_value('MAX_ERROR_PERCENT'))

    if len(logs_stats) == 0:
        logging.info('Don`t have enough data for generate report')
        return

    logging.info('Generating report')
    report_path = report.generate_report(logs_stats, log['date'], int(config.get_value('REPORT_SIZE')))
    logging.info(f'See report in {report_path}')
