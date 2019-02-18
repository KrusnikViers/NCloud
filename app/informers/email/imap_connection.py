import imaplib
import logging

from app.informers.email.params import Parameters


class ImapConnection:
    def __init__(self, params: Parameters):
        self._params = params
        self._client = None

    def __enter__(self):
        logging.debug('Establishing email server connection...')
        self._client = imaplib.IMAP4_SSL(self._params.server)
        return self

    # Returns unread count (if fetched) and error string (empty, if everything is OK)
    def get_unread_count(self) -> (int, str):
        logging.debug('Trying to fetch unread emails count...')
        self._client.login(self._params.login, self._params.password)
        self._client.select(readonly=True)
        status_code, response = self._client.search(None, '(UNSEEN)')
        result = 0
        error = ''
        if status_code == 'OK':
            result = len(response[0].split())
        else:
            error = 'Email was not fetched: {} - {}'.format(status_code, response)
            logging.error(error)
        self._client.close()
        return result, error

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.logout()
