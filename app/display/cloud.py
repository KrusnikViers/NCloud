import logging

from RPi import GPIO

from app.display.diode import DiodeOutput


class Cloud:
    # Constants for actual pins. Pins are numbered in sections row by row from top, from left to right.
    SUN_OUT = [16, 19, 13]
    CLOUD_OUT = [18, 26, 24, 15, 21, 12, 10, 17, 14]
    CLOUD_IN = [8, 4, 3, 2]

    ERRORS_OUT = 18

    def __init__(self):
        self.state_map = {}

    def stop(self, pin: int):
        if pin in self.state_map:
            self.state_map[pin].stop()
            del self.state_map[pin]

    def set(self, pin: int, lighted: bool = False, lighted_partial: float = None, pwm_state: tuple = None):
        self.stop(pin)
        self.state_map[pin] = DiodeOutput(pin, lighted, lighted_partial, pwm_state)

    @classmethod
    def enter(cls):
        logging.info('Initializing GPIO Cloud')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(cls.SUN_OUT + cls.CLOUD_OUT, GPIO.OUT)
        GPIO.output(cls.SUN_OUT + cls.CLOUD_OUT, False)
        GPIO.setup(cls.CLOUD_IN, GPIO.IN)

    @staticmethod
    def exit(self):
        logging.info('GPIO Cloud shutdown')
        GPIO.cleanup()
