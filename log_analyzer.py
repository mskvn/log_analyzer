from log_analyzer.log_analyzer import log_analyze


def main():
    try:
        log_analyze()
    except Exception as e:
        print(e)  # TODO: logger


if __name__ == "__main__":
    main()
