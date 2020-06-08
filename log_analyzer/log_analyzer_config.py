import json
import os


class LogAnalyzerConfig:
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'config.json')

    def __init__(self, custom_config_path=None):
        self._defaults = self._init_defaults()
        self._customs = self._init_custom(custom_config_path)

    def get_value(self, name):
        if name in self._customs:
            return self._customs[name]
        if name in self._defaults:
            return self._defaults[name]
        return None

    def _init_custom(self, custom_config_path):
        if custom_config_path:
            return self._load_configs(custom_config_path)
        else:
            return dict()

    def _init_defaults(self):
        return self._load_configs(self.DEFAULT_CONFIG_PATH)

    @staticmethod
    def _load_configs(config_path):
        with open(config_path, 'r') as json_file:
            return json.load(json_file)
