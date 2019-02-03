import argparse
import json
import logging
import os
import pathlib

_ROOT_DIR = pathlib.Path(os.path.realpath(__file__)).parent.parent.parent


class Configuration:
    def __init__(self):
        self.location = None
        self.ipinfo_token = None
        self.none = None

    @classmethod
    def load(cls):
        args = cls._get_command_line_arguments()
        json_config = cls._get_configuration_file_content(args.configuration_file)

        def maybe_get_value(option_name: str):
            value = getattr(args, option_name)
            return value if value else json_config.get(option_name, None)

        instance = cls()
        instance.location = cls._parse_location(maybe_get_value('lat'), maybe_get_value('lon'))
        instance.ipinfo_token = maybe_get_value('ipinfo_token')
        return instance

    @staticmethod
    def _get_command_line_arguments() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Informer application for Raspberry Pi.')
        parser.add_argument('--configuration-file', '-c', type=str, default=str(_ROOT_DIR) + '/configuration.json',
                            dest='configuration_file', help='Json-formatted file with configuration.')
        parser.add_argument('--latitude', '-lat', type=float, dest='lat', help='Latitude for sun informer.')
        parser.add_argument('--longitude', '-lon', type=float, dest='lon', help='Longitude for sun informer.')
        parser.add_argument('--ipinfo-token', '-it', type=str, dest='ipinfo_token', help='IPInfo.io token.')
        return parser.parse_args()

    @staticmethod
    def _parse_location(lat, lon) -> (float, float):
        return (float(lat), float(lon)) if lat and lon else None

    @staticmethod
    def _get_configuration_file_content(configuration_file_path: str) -> dict:
        file_location_path = pathlib.Path(configuration_file_path)
        if file_location_path.is_file():
            with file_location_path.open() as configuration_file:
                return json.load(configuration_file)
        logging.info('Configuration file is missing, using only command line parameters.')
        return {}
