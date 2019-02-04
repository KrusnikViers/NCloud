import imaplib
import logging

from app.core.configuration import Configuration


class EmailUnreadFetcher:
    def __init__(self, configuration: Configuration):
        self._server = configuration.get("email.imap_server", str)
        self._login = configuration.get("email.login", str)
        self._password = configuration.get("email.password", str)
        self.is_available = self._server and self._client and self._password
        self._client = None
        self.unread_count = 0

    def __enter__(self):
        logging.info('Fetching unread emails...')
        self._client = imaplib.IMAP4_SSL(self._server)
        self._client.login(self._login, self._password)
        self._client.select(readonly=True)

    def fetch(self):
        status_code, response = self._client.search(None, 'INBOX', '(UNSEEN)')
        if status_code == 'OK':
            self.unread_count = len(response[0].split())

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.logout()
