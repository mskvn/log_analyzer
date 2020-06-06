# Log analyzer

Parse nginx logs and build html report with statistics

## Requirements

* python 3.6+

## Usage

Run with default configs (`log_analyzer/configs/config.json`)

```shell script
python log_analyzer.py 
```

Run with custom configs

```shell script
python log_analyzer.py --configs /paht/to/configs.json
```

Config example

```json
{
  "REPORT_SIZE": 1000,
  "REPORT_DIR": "./reports",
  "LOG_DIR": "./logs",
  "MAX_ERROR_PERCENT": 0.1
}

```

## Development

### Tests

For run tests
```shell script
python -m unittest discover tests
```