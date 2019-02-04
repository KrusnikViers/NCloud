import argparse
import json
import logging
import os
import pathlib

_ROOT_DIR = pathlib.Path(os.path.realpath(__file__)).parent.parent.parent


class Configuration:
    def __init__(self):
        self.data = {}

    @classmethod
    def load(cls):
        instance = Configuration()
        args, overrides = cls._get_command_line_arguments()
        instance.data = cls._get_configuration_file_content(args.configuration_file)
        instance._apply_overrides(overrides)

        return instance

    def get(self, path: str, value_type, default=None):
        current_dict, last_key = self._resolve_dict(path)
        if last_key in current_dict:
            return value_type(current_dict[last_key])
        return default

    @staticmethod
    def _get_command_line_arguments() -> (argparse.Namespace, list):
        parser = argparse.ArgumentParser(description='Informer application for Raspberry Pi.')
        parser.add_argument('--configuration-file', '-c', type=str, default=str(_ROOT_DIR) + '/configuration.json',
                            dest='configuration_file', help='Json-formatted file with configuration.')
        return parser.parse_known_args()

    @staticmethod
    def _get_configuration_file_content(configuration_file_path: str) -> dict:
        file_location_path = pathlib.Path(configuration_file_path)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                return json.load(configuration_file)
        logging.info('Configuration file is missing, using only command line parameters.')
        return {}

    def _resolve_dict(self, path: str) -> (dict, str):
        key_sequence = path.split('.')
        last_key = key_sequence[-1]
        current_dict = self.data
        for key in key_sequence[:-1]:
            if key not in current_dict:
                current_dict[key] = dict()
            current_dict = current_dict[key]
        return current_dict, last_key

    def _apply_overrides(self, overrides: list):
        for override in overrides:
            key, value = override.split('=')
            current_dict, last_key = self._resolve_dict(key)
            current_dict[last_key] = value
