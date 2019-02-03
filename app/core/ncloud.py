import logging
import time

from app.components.cloud import Cloud
from app.components.location import Location
from app.core.configuration import Configuration


class NCloud:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.INFO)

        self.configuration = Configuration.load()
        self.location = Location(self.configuration)

    def run(self):
        with Cloud() as cloud:
            cloud.set(cloud.SUN_OUT, True)
            time.sleep(5)
