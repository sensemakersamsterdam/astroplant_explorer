"""
ae_drivers AE_PWM_LED code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral, GPIO


class AE_PWM_LED(_AE_Peripheral):
    """This class is to define a PWM-LED.
    """

    def __init__(self, name, description, pin, initial_state=None, frequency=None):
        assert pin.__class__.__name__ == 'AE_Pin' and pin.value[
            2] == 'GPIO', 'Specify parameter "pin" as AE_Pin GPIO enum.'
        assert initial_state is None or (
            0 <= int(initial_state) <= 100), "Initial state between 0 and 100 inclusive."
        assert frequency is None or (
            30 <= int(frequency) <= 2000), "Frequency between 30 and 2000 inclusive."
        super().__init__(name, description, 'PWM-LED')
        self._pin = pin
        if initial_state is not None:
            self._dc = int(initial_state)
        else:
            self._dc = 0  # Default LED is off
        if frequency is not None:
            self._frequency = int(frequency)
        else:
            self._frequency = 100  # 100 Hz default
        self._pled = None

    def _str_details(self):
        return 'pin %s(gpio=%d, conn=%d), value=%s' % (self._pin.name,
                                                       self._pin.value[0], self._pin.value[1],
                                                       self.value())

    def value(self, set_to=None):
        assert self._pled is not None, 'Use set-up for PWM-LED first'
        if set_to is not None:
            assert 0 <= int(
                set_to) <= 100, "set_to value between 0 and 100 inclusive."
            self._dc = abs(int(set_to)) % 101   # Limit to 0 <= integer <= 100
            self._pled.ChangeDutyCycle(self._dc)
        # Now read back the value
        return self._dc

    def setup(self, **kwarg):
        GPIO.setup(self._pin.value[0], GPIO.OUT)
        GPIO.output(self._pin.value[0], 0)
        self._pled = GPIO.PWM(self._pin.value[0], self._frequency)
        self._pled.start(0)

        initial_state = kwarg.get('initial_state', self._dc)
        self.value(initial_state)

    def on(self):
        return self.value(100)

    def off(self):
        return self.value(0)

    def toggle(self):
        if self.is_on():
            self.off()
        else:
            self.on()

    def __del__(self):
        if self._pled is not None:
            self._pled.stop()
            self._pled = None
