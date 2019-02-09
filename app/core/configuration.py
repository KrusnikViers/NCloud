import argparse
import json
import logging
import os
import pathlib

_ROOT_DIR = pathlib.Path(os.path.realpath(__file__)).parent.parent.parent


class Configuration:
    def __init__(self):
        self._data = {}
        self.is_debug = False

    @classmethod
    def load(cls):
        instance = Configuration()
        args, overrides = cls._get_command_line_arguments()
        instance.is_debug = args.is_debug
        file_location_path = pathlib.Path(args.configuration_file)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                instance._data = json.load(configuration_file)
        else:
            logging.warning('Configuration file not found!')
        instance._apply_overrides(overrides)

        return instance

    def get(self, path: str, value_type, default=None):
        current_dict, key = self._get_dict_and_key_name(path)
        return value_type(current_dict.get(key, default))

    @staticmethod
    def _get_command_line_arguments() -> (argparse.Namespace, list):
        parser = argparse.ArgumentParser()
        parser.add_argument('--configuration-file', '-c', type=str, default=str(_ROOT_DIR) + '/configuration.json',
                            dest='configuration_file', help='Json-formatted file with configuration.')
        parser.add_argument('--debug', action='store_true', dest='is_debug', help='Show debug output.')
        return parser.parse_known_args()

    def _get_dict_and_key_name(self, full_path: str) -> (dict, str):
        key_sequence = full_path.split('.')
        last_key = key_sequence[-1]
        current_dict = self._data
        for key in key_sequence[:-1]:
            current_dict = current_dict[key] if key in current_dict else {}
        return current_dict, last_key

    def _apply_overrides(self, overrides: list):
        for override in overrides:
            full_key_path, value = override.split('=')
            current_dict, key = self._get_dict_and_key_name(full_key_path)
            current_dict[key] = value
