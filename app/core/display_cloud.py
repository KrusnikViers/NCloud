import logging

from RPi import GPIO as gpio


class DisplayCloud:
    # Constants for actual pins. Pins are numbered in sections row by row from top, from left to right.
    SUN_OUT = [16, 19, 13]
    CLOUD_OUT = [18,
                 26, 24, 15,
                 21, 12, 10, 17, 14]
    CLOUD_IN = [8, 4, 3, 2]

    @staticmethod
    def set(pin_or_pins, value: bool):
        gpio.output(pin_or_pins, value)

    def __enter__(self):
        logging.info('Initializing GPIO Cloud')
        gpio.setmode(gpio.BCM)
        gpio.setup(self.SUN_OUT + self.CLOUD_OUT, gpio.OUT)
        gpio.setup(self.CLOUD_IN, gpio.IN)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('Cleaning GPIO Cloud')
        gpio.cleanup()
