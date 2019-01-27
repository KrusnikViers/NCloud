from app import cloud

import time

try:
    cloud.initialize()
    time.sleep(3)
finally:
    cloud.cleanup()
