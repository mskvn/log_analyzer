import argparse
import logging

from log_analyzer.log_analyzer import log_analyze
from log_analyzer.log_analyzer_config import LogAnalyzerConfig


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze nginx logs')
    parser.add_argument('--config', type=str,
                        help='path to custom configs')
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        config = LogAnalyzerConfig(custom_config_path=args.config)  # TODO: custom_config_path from --config param
        logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                            datefmt='%Y.%m.%d %H:%M:%S',
                            filename=config.get_value('LOG_FILE'),
                            filemode='a',
                            level=logging.INFO
                            )
        log_analyze(config)
    except Exception:
        logging.exception("Exception occurred")


if __name__ == "__main__":
    main()
