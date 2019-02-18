import logging
import multiprocessing
import queue
import signal

from app.core.configuration import Configuration
from app.display.interface import Interface
from app.core.notifications import Notification

from app.informers import email


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
        self.informers = list

    def run(self):
        logging.info('Application start')

        logging.info('Launching informers...')

        logging.info('Launching main cycle...')
        with Interface() as display:
            self.display = display
            self._main_cycle()

        logging.info('Terminating informers...')
        for informer in self.informers.values():
            informer.terminate()
        logging.info('Application shutdown')

    def _main_cycle(self):
        handlers = {
            Notification.EMAIL: self.display.update_email_count,
        }

        while True:
            try:
                notification = self.queue.get(timeout=self.LOOP_PERIOD_SECONDS)
                handlers[notification.type](notification)
            except queue.Empty:
                pass
            if self.was_interrupted:
                break

    def _set_exit_flag(self, *args):
        self.was_interrupted = True
