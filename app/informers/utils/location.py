import json
import logging

import requests


def fetch(ipinfo_token: str) -> list:
    logging.info('Requesting current location from IPInfo...')
    try:
        ip_location = requests.get('https://ipinfo.io/json?token={}'.format(ipinfo_token)).text
        ip_location_json = json.loads(ip_location)
    except requests.exceptions.RequestException as e:
        logging.error('IPInfo request failure: {}'.format(e))
        return []

    logging.info('Your location resolved as {country}, {region}, {city} ({loc})'.format(**ip_location_json))
    coordinates = [float(x) for x in ip_location_json['loc'].split(',')]
    return coordinates
