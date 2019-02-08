import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from app.core.configuration import Configuration


class TestConfiguration(TestCase):
    test_configuration = Path(os.path.realpath(__file__)).parent.joinpath('data', 'configuration.json')

    @patch('sys.argv', ['_', '-c', str(test_configuration)])
    def test_read_from_file(self):
        config = Configuration.load()
        self.assertEqual(180.634, config.get('location.lat', float))
        self.assertEqual(50.0, config.get('location.lon', float))
        self.assertEqual('abcdef', config.get('location.ipinfo_token', str))
        self.assertEqual('email@example.com', config.get('email.login', str))
        self.assertEqual('password', config.get('email.password', str))

    @patch('sys.argv', ['_', '-c', str(test_configuration), 'location.lat=222.22'])
    def test_command_line_override(self):
        config = Configuration.load()
        self.assertEqual(222.22, config.get('location.lat', float))
        self.assertEqual(50.0, config.get('location.lon', float))
        self.assertEqual('abcdef', config.get('location.ipinfo_token', str))
        self.assertEqual('email@example.com', config.get('email.login', str))
        self.assertEqual('password', config.get('email.password', str))

    @patch('sys.argv', ['_', '-c', str(test_configuration)])
    def test_default_get(self):
        config = Configuration.load()
        self.assertEqual(180.634, config.get('location.lat', float))
        self.assertEqual(50.0, config.get('location.lon', float))
        self.assertEqual('abcdef', config.get('location.ipinfo_token', str))
        self.assertEqual('email@example.com', config.get('email.login', str))
        self.assertEqual('password', config.get('email.password', str))
        self.assertEqual('imap.google.com', config.get('email.imap_server', str, 'imap.google.com'))
