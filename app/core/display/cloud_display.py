import logging

from RPi import GPIO as gpio

from app.core.display.diode_state import DiodeState


class CloudDisplay:
    # Constants for actual pins. Pins are numbered in sections row by row from top, from left to right.
    _SUN_OUT = [16, 19, 13]
    _CLOUD_TOP_OUT = [18]
    _CLOUD_MIDDLE_OUT = [26, 24, 15]
    _CLOUD_BOTTOM_OUT = [21, 12, 10, 17, 14]
    _CLOUD_IN = [8, 4, 3, 2]

    # Flashes, when some errors are waiting in notifications list.
    ERRORS_CHANNEL = _CLOUD_BOTTOM_OUT[0]
    # Write error messages in log and stop flashing.
    ERRORS_CONTROL_CHANNEL = _CLOUD_IN[0]

    EMAIL_CHANNEL = _CLOUD_BOTTOM_OUT[4]

    # Turn on/off all the lights on the board.
    LIGHT_CONTROL_CHANNEL = _CLOUD_IN[3]

    def __init__(self):
        self.state_map = {}

    def set(self, pin: int, value: bool = False, pwm_state: tuple = None):
        if pin in self.state_map:
            self.state_map[pin].stop()
        self.state_map[pin] = DiodeState(pin, value, pwm_state)

    def __enter__(self):
        logging.info('Initializing GPIO Cloud')
        gpio.setmode(gpio.BCM)
        out_channels = self._SUN_OUT + self._CLOUD_TOP_OUT + self._CLOUD_MIDDLE_OUT + self._CLOUD_BOTTOM_OUT
        gpio.setup(out_channels, gpio.OUT)
        gpio.output(out_channels, False)
        gpio.setup(self._CLOUD_IN, gpio.IN)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info('GPIO Cloud shutdown')
        gpio.cleanup()
