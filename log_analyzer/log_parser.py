# log_format ui_short '$remote_addr $remote_user  $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import gzip


class LogParser:

    @staticmethod
    def parse_log(log):
        open_func = gzip.open if log['ext'] == 'gz' else open
        open_func(log['path'], encoding="ascii", errors="surrogateescape")
        # fields = [x.strip() for x in line.split(" ")]
