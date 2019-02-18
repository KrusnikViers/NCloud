from RPi import GPIO


_DEFAULT_PWM_FREQUENCY = 144.


class DiodeState:
    def __init__(self, channel: int, lighted: bool = False, lighted_partial: float = None, pwm_frequency: float = None,
                 pwm_duty=None):
        self.channel = channel
        self.lighted = lighted
        self.lighted_partial = lighted_partial
        self.pwm_frequency = pwm_frequency
        self.pwm_duty = pwm_duty

    @classmethod
    def stable(cls, channel: int, value: bool = True):
        return cls(channel, lighted=value)

    @classmethod
    def partial(cls, channel: int, value: float = 0.5):
        return cls(channel, lighted_partial=value)

    @classmethod
    def flicker(cls, channel: int, frequency: float = _DEFAULT_PWM_FREQUENCY, duty: float = 1):
        return cls(channel, pwm_frequency=frequency, pwm_duty=duty)


class DiodeOutput:
    def __init__(self, diode_state: DiodeState):
        self.channel = diode_state.channel
        self.pwm_mode = None
        if diode_state.pwm_frequency and diode_state.pwm_duty:
            self.pwm_mode = GPIO.PWM(self.channel, diode_state.pwm_frequency)
            self.pwm_mode.start(diode_state.pwm_duty)
        elif diode_state.lighted_partial:
            self.pwm_mode = GPIO.PWM(self.channel, _DEFAULT_PWM_FREQUENCY)
            self.pwm_mode.start(diode_state.lighted_partial * 100.)
        else:
            GPIO.output(self.channel, diode_state.lighted)

    def stop(self):
        if self.pwm_mode:
            self.pwm_mode.stop()
        else:
            GPIO.output(self.channel, False)