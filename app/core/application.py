import logging
import multiprocessing
import queue
import signal

from app.core.configuration import Configuration
from app.core.display.cloud_display import CloudDisplay
from app.core.notifications import Notification
from app.informers.email import EmailInformer


class Application:
    LOOP_PERIOD_SECONDS = 1

    def __init__(self):
        log_pattern = '%(asctime)s:%(name)s:%(levelname)s - %(message)s'
        logging.basicConfig(format=log_pattern, level=logging.INFO)

        # True, if SIGINT or SIGTERM was received.
        self.was_interrupted = False
        for signal_type in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(signal_type, self._set_exit_flag)

        # Display module (Amperka GPIO Cloud in our case)
        self.display = None

        # Application configuration
        self.configuration = Configuration.load()
        if self.configuration.is_debug:
            logging.basicConfig(format=log_pattern, level=logging.DEBUG)

        # Main events queue, filled with |app.core.notifications.Notification| instances
        mp_manager = multiprocessing.Manager()
        self.queue = mp_manager.Queue()

        # Informers
        self.informers = {
            'email': EmailInformer(self.configuration, self.queue)
        }

        # Handlers
        self.handlers = {
            Notification.EMAIL: self._on_email_notification,
        }

    def run(self):
        logging.info('Application start')

        logging.info('Launching informers...')
        for informer in self.informers.values():
            informer.start()

        logging.info('Launching main cycle...')
        with CloudDisplay() as display:
            self.display = display
            self.main_cycle()

        logging.info('Terminating informers...')
        for informer in self.informers.values():
            informer.terminate()
        logging.info('Application shutdown')

    def main_cycle(self):
        while True:
            try:
                notification = self.queue.get(timeout=self.LOOP_PERIOD_SECONDS)
                self.handlers[notification.type](notification)
            except queue.Empty:
                pass
            if self.was_interrupted:
                break

    def _on_email_notification(self, notification: Notification):
        self.display.set(CloudDisplay.EMAIL_CHANNEL, notification.params.get('unread', 0) != 0)

    def _set_exit_flag(self, *args):
        self.was_interrupted = True
