import imaplib
import logging
import multiprocessing
import time

from app.core.notifications import Notification
from app.informers.email.imap_connection import ImapConnection
from app.informers.email.params import Parameters
from app.informers.utils.subprocess import Subprocess


class Informer(Subprocess):
    def _get_process_info(self):
        return {
            'name': 'email_informer',
            'is_enabled': True,
            'target': self.fetcher_process,
            'args': (self._channel, self._queue, self._params)
        }

    def __init__(self, channel: int, queue: multiprocessing.Queue, params_dict: dict):
        self._channel = channel
        self._params = Parameters.from_dict(params_dict)
        self._queue = queue
        super(Informer, self).__init__()

    @classmethod
    def fetcher_process(cls, channel: int, params: Parameters, queue: multiprocessing.Queue):
        while True:
            with ImapConnection(params) as connection:
                try:
                    unread_count = connection.get_unread_count()
                    logging.debug('Email fetched, unread count: {}'.format(unread_count))
                    queue.put(Notification(Notification.EMAIL, {'channel': channel, 'unread': unread_count}))
                except imaplib.IMAP4.error as e:
                    error_string = 'Email fetcher failed: {}'.format(e)
                    logging.error(error_string)
                    queue.put(Notification(Notification.ERROR, {"error": error_string}))
            time.sleep(params.period)
