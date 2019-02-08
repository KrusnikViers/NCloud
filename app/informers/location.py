import json
import logging

import requests

from app.core.configuration import Configuration


class Location:
    def __init__(self, config: Configuration):
        self.latitude = 0.
        self.longitude = 0.
        # True, if location has loaded coordinates.
        self.is_available = False

        self._load(config)
        if not self.is_available:
            logging.warning('Location was not initialized, sun informer will be unavailable')

    def _load(self, config: Configuration):
        configured_latitude = config.get("location.lat", float)
        configured_longitude = config.get("location.lon", float)
        if configured_latitude and configured_longitude:
            self.latitude = configured_latitude
            self.longitude = configured_longitude
            self.is_available = True
            logging.info('Location was set from config: {}:{}'.format(self.latitude, self.longitude))

        ipinfo_token = config.get("location.ipinfo_token", str)
        if not self.is_available and ipinfo_token:
            requested_location = self._request_geolocation(ipinfo_token)
            if requested_location:
                self.latitude, self.longitude = requested_location
                self.is_available = True

    @staticmethod
    def _request_geolocation(ipinfo_token: str) -> (float, float):
        logging.info('Requesting current location from IPInfo...')
        try:
            ip_location = requests.get('https://ipinfo.io/json?token={}'.format(ipinfo_token)).text
            ip_location_json = json.loads(ip_location)
        except requests.exceptions.RequestException as e:
            logging.error('IPInfo requesting failure: {}'.format(e))
            return

        logging.info('Your location resolved as {country}, {region}, {city} ({loc})'.format(**ip_location_json))
        coordinates = [float(x) for x in ip_location_json['loc'].split(',')]
        return coordinates[0], coordinates[1]
