import logging

from log_analyzer.log_analyzer import log_analyze
from log_analyzer.log_analyzer_config import LogAnalyzerConfig


def main():
    try:
        config = LogAnalyzerConfig()  # TODO: custom_config_path from --config param
        logging.basicConfig(format='[%(asctime)s] %(levelname).1s %(message)s',
                            datefmt='%Y.%m.%d %H:%M:%S',
                            filename=config.get_value('LOG_FILE'),
                            filemode='w+',
                            level=logging.INFO
                            )
        log_analyze(config)
    except Exception:
        logging.exception("Exception occurred")


if __name__ == "__main__":
    main()
