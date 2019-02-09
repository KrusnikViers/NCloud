import imaplib
import logging
import multiprocessing
import time

from app.core.configuration import Configuration
from app.core.notifications import Notification
from app.informers.utils.subprocess import Subprocess


class EmailInformer(Subprocess):
    def __init__(self, configuration: Configuration, queue: multiprocessing.Queue):
        self._config = {
            'server': configuration.get('email.imap_server', str),
            'login': configuration.get('email.login', str),
            'password': configuration.get('email.password', str),
            'period': configuration.get('email.update_period_seconds', float, 30.0)
        }
        self._queue = queue
        super(EmailInformer, self).__init__()

    def _get_process_info(self):
        return {
            'name': 'email_informer',
            'is_enabled': self._config['server'] and self._config['login'] and self._config['password'],
            'target': EmailInformer.fetcher_process,
            'args': (self._config, self._queue)
        }

    class _ImapConnection:
        def __init__(self, inner_configuration: dict):
            self._config = inner_configuration
            self._client = None

        def __enter__(self):
            logging.debug('Establishing email server connection...')
            self._client = imaplib.IMAP4_SSL(self._config['server'])
            return self

        def get_unread_count(self) -> int:
            logging.debug('Trying to fetch unread emails count...')
            self._client.login(self._config['login'], self._config['password'])
            self._client.select(readonly=True)
            status_code, response = self._client.search(None, '(UNSEEN)')
            result = 0
            if status_code == 'OK':
                result = len(response[0].split())
            else:
                logging.error('Email was not fetched: {} - {}'.format(status_code, response))
            self._client.close()
            return result

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._client.logout()

    @classmethod
    def fetcher_process(cls, config: dict, queue: multiprocessing.Queue):
        while True:
            with cls._ImapConnection(config) as connection:
                try:
                    unread_count = connection.get_unread_count()
                    logging.debug('Email fetched, unread count: {}'.format(unread_count))
                    queue.put(Notification(Notification.EMAIL, {'unread': unread_count}))
                except imaplib.IMAP4.error as e:
                    logging.error('Email fetcher failed: {}'.format(e))
            time.sleep(config['period'])
