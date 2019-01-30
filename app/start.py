import logging
import time

from app.components.cloud import Cloud


logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s - %(message)s', level=logging.DEBUG)
with Cloud() as cloud:
    cloud.set(cloud.SUN_OUT, True)
    time.sleep(5)
