from app.display.cloud import Cloud
from app.core.notifications import Notification
import logging


class Interface:
    def __init__(self):
        self.display = Cloud()

        self.pending_errors = list()

        self.email_count = 0

    def __enter__(self):
        self.display.enter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.display.exit()

    def _check_errors(self, notification: Notification):
        if notification.error_string:
            logging.error(notification.error_string)
            self.pending_errors.append(notification.error_string)
            self.display.set(Cloud.CLOUD_TOP_OUT[0], pwm_state=(0.2, 1))

    def update_email_count(self, notification: Notification):
        self._check_errors(notification)
        self.display.set(Cloud.CLOUD_MIDDLE_OUT[2], lighted=notification.params.get('unread', 0) != 0)
