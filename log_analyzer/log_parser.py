import gzip
import logging
import re
from statistics import median


class LogParser:
    # log_format ui_short '$remote_addr $remote_user  $http_x_real_ip [$time_local] "$request" '
    #                     '$status $body_bytes_sent "$http_referer" '
    #                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
    #                     '$request_time';

    LOG_REGEXP = re.compile(r'^\S+ \S+\s+\S+ \[\S+ \S+\] "\S+ (?P<target>\S+) \S+" '
                            r'\S+ \S+ "\S+" '
                            r'".+?" "\S+" "\S+" "\S+" '
                            r'(?P<time>\S+)$')

    def parse_log(self, log, max_errors_percent):
        """
        Parse nginx log file and return list of dicts with stats by each url
        Stats contains few keys: url, count, count_perc, time_avg, time_med, time_max, time_sum, time_perc
        :param log: dict
        :param max_errors_percent: float
        Dict with two required keys:
        path: path to log file
        ext: log file extension
        :return: list
        """
        result = self._calc_raw_stats(log)
        if result['errors_perc'] >= max_errors_percent:
            logging.info(f"{result['errors_perc']} % of line did not process")
            return list()
        logging.info('Raw stats collect. Calculating metrics for report now.')
        return self._calc_report_stats(result['raw_stats'], result['total_count'], result['total_time'])

    def _calc_report_stats(self, raw_stats, total_count, total_time):
        report_stats = list()
        for url, url_stat in raw_stats.items():
            times_sum = sum(url_stat['time'])
            times_len = len(url_stat['time'])
            report_stats.append({
                'url': url,
                'count': len(url_stat['time']),
                'count_perc': round((times_len / total_count) * 100, 3),
                'time_avg': round(times_sum / times_len, 3),
                'time_med': round(median(url_stat['time']), 3),
                'time_max': round(max(url_stat['time']), 3),
                'time_sum': round(times_sum, 3),
                'time_perc': round((times_sum / total_time) * 100, 3)

            })
        return report_stats

    def _calc_raw_stats(self, log):
        stats = dict()
        total_time = 0
        total_count = 0
        errors = 0
        lines_count = 0
        for line in self._parsed_lines(log):
            lines_count += 1
            if not line:
                errors += 1
            else:
                if line['url'] not in stats:
                    stats[line['url']] = {'time': list()}
                stats[line['url']]['time'].append(line['time'])
                total_count += 1
                total_time += line['time']
        logging.info(f'Processed {lines_count} lines')
        logging.info(f'{errors} line was skipped')
        return {
            'raw_stats': stats,
            'total_count': total_count,
            'total_time': total_time,
            'errors_perc': errors / lines_count
        }

    def _parsed_lines(self, log):
        open_func = gzip.open if log['ext'] == 'gz' else open
        with open_func(log['path'], mode='rb') as f:
            for line in f:
                yield self._process_line(line)

    def _process_line(self, line):
        line = line.decode(encoding="ascii", errors="surrogateescape")
        match = re.search(self.LOG_REGEXP, line)
        if not match:
            logging.debug(f"Log line not match with regexp:\n{line}")
            return None
        target = match.group('target')
        return {'url': target, 'time': float(match.group('time'))}
