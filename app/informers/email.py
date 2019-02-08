import imaplib
import logging
import multiprocessing
import time

from app.core.configuration import Configuration
from app.core.notifications import Notification


class EmailInformer:
    # |handler_function|: f(int unread_emails)
    def __init__(self, configuration: Configuration, queue: multiprocessing.Queue):
        self._config = {
            'server': configuration.get('email.imap_server', str),
            'login': configuration.get('email.login', str),
            'password': configuration.get('email.password', str),
            'period': configuration.get('email.update_period_seconds', float, 60.0)
        }
        self.is_available = self._config['server'] and self._config['login'] and self._config['password']
        self._process = None
        self._queue = queue

    def start(self):
        self._process = multiprocessing.Process(target=self.fetcher_process,
                                                name='email daemon',
                                                args=(EmailInformer, self._config, self._queue))
        self._process.daemon = True
        self._process.start()

    class _EmailServerConnection:
        def __init__(self, inner_configuration: dict):
            self._config = inner_configuration
            self._client = None

        def __enter__(self):
            self._client = imaplib.IMAP4_SSL(self._config['server'])
            self._client.login(self._config['login'], self._config['password'])

        def get_unread_count(self) -> int:
            self._client.select(readonly=True)
            status_code, response = self._client.search(None, 'INBOX', '(UNSEEN)')
            result = 0
            if status_code == 'OK':
                result = len(response[0].split())
            self._client.close()
            return result

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._client.logout()

    @classmethod
    def fetcher_process(cls, config: dict, queue: multiprocessing.Queue):
        while True:
            with cls._EmailServerConnection(config) as connection:
                unread_count = connection.get_unread_count()
                logging.debug('Email fetched, unread count: {}'.format(unread_count))
                queue.put(Notification(Notification.EMAIL, {'unread': unread_count}))
            time.sleep(config['period'])
