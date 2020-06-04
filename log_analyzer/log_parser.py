import gzip
import re
from statistics import median


class LogParser:
    # log_format ui_short '$remote_addr $remote_user  $http_x_real_ip [$time_local] "$request" '
    #                     '$status $body_bytes_sent "$http_referer" '
    #                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
    #                     '$request_time';
    LOG_REGEXP = r'(.+)\s+(.+)\s+(.+)\s+\[(.+)\]\s+"(?P<request>.+)"' \
                 r'\s+(.+)\s+(.+)\s+"(.+)"' \
                 r'\s+"(.+)"\s+"(.+)"\s+"(.+)"\s+"(.+)"' \
                 r'\s+(?P<time>.+)'

    def parse_log(self, log):
        """
        Parse nginx log file and return list of dicts with stats by each url
        Also return percent of unparsed rows
        Stats contains few keys: url, count, count_perc, time_avg, time_med, time_max, time_sum, time_perc
        :param log: dict
        Dict with two required keys:
        path: path to log file
        ext: log file extension
        :return: tuple
        """
        result = self._calc_raw_stats(log)
        report_stats = self._calc_report_stats(result['raw_stats'], result['total_count'], result['total_time'])
        return report_stats, result['errors_perc']

    def _calc_report_stats(self, raw_stats, total_count, total_time):
        report_stats = list()
        for url, url_stat in raw_stats.items():
            times_sum = sum(url_stat['time'])
            times_len = len(url_stat['time'])
            report_stats.append({
                'url': url,
                'count': len(url_stat['time']),
                'count_perc': round(times_len / total_count, 3),
                'time_avg': round(times_sum / times_len, 3),
                'time_med': median(url_stat['time']),
                'time_max': max(url_stat['time']),
                'time_sum': times_sum,
                'time_perc': round(times_sum / total_time, 3)

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
            print(f"Log line not match with regexp:\n{line}")  # TODO: logger
            return None
        request = match.group('request')
        if len(request.split()) != 3:
            print(f"Wrong $request format: {request}")  # TODO: logger
            return None
        return {'url': request.split()[1], 'time': float(match.group('time'))}
