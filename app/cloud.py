from RPi import GPIO as gpio


# Creating constants for actual pins. Pins are numbered in sections row by row from top, from left to right.
SUN_OUT = [16, 19, 13]
CLOUD_OUT = [18,
             26, 24, 15,
             21, 12, 10, 17, 14]
CLOUD_IN = [8, 4, 3, 2]


def initialize():
    # Initializing all Amperka GPIO Cloud pins:
    gpio.setmode(gpio.BCM)
    gpio.setup(SUN_OUT + CLOUD_OUT, gpio.OUT)
    gpio.setup(CLOUD_IN, gpio.IN)

    gpio.output(SUN_OUT, True)


def cleanup():
    gpio.cleanup()
