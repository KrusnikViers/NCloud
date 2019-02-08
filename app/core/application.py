import logging
import time
import multiprocessing

from app.core.configuration import Configuration
from app.core.display_cloud import DisplayCloud
from app.informers.location import Location
from app.informers.email import EmailInformer


class Application:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)

        self.configuration = Configuration.load()
        self.location = Location(self.configuration)
        self.queue = multiprocessing.Queue()

        self.email_informer = EmailInformer(self.configuration, self.queue)

    def run(self):
        logging.info('Application start')
        logging.info('Launching informers...')
        self.email_informer.start()
        logging.info('Launching main cycle...')
        with DisplayCloud() as cloud:
            cloud.set(cloud.SUN_OUT, True)
            time.sleep(5)
        logging.info('Application end')
