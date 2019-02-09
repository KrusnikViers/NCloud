from RPi import GPIO as gpio


class DiodeState:
    def __init__(self, channel: int, value: bool = False, pwm_mode: tuple = None):
        self.channel = channel
        self.pwm_mode = None
        if pwm_mode:
            frequency, duty_cycle = pwm_mode
            self.pwm_mode = gpio.PWM(channel, frequency)
            self.pwm_mode.start(duty_cycle)
        else:
            gpio.output(channel, value)

    def stop(self):
        if self.pwm_mode:
            self.pwm_mode.stop()
        else:
            gpio.output(self.channel, False)
