import json
import logging
import os


class LogAnalyzerConfig:
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs', 'config.json')

    def __init__(self, custom_config_path=None):
        self.__init_defaults()
        self.__customs = self.__init_custom(custom_config_path)
        logging.info("Default configs:\n{}\nCustom configs:\n{}".format(self.__defaults, self.__customs))

    def get_value(self, name):
        if name in self.__customs:
            return self.__customs[name]
        if name in self.__defaults:
            return self.__defaults[name]
        return None

    def __init_custom(self, custom_config_path):
        if custom_config_path:
            return self.__init_defaults()
        else:
            return dict()

    def __init_defaults(self):
        return self.__load_configs(self.DEFAULT_CONFIG_PATH)

    def __load_configs(self, config_path):
        with open(config_path, 'r') as json_file:
            self.__defaults = json.load(json_file)
