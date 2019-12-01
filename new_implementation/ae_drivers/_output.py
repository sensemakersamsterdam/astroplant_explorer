# ToDo: copyright etc.
from . import _AE_Peripheral, GPIO


class _AE_Output(_AE_Peripheral):
    """Base class for an/off actuators like regular LEDs and Relays.
    """

    def __init__(self, name, description, type_, pin, initial_state=None):
        assert pin.__class__.__name__ == 'AE_Pin' and pin.value[
            2] == 'GPIO', 'Specify parameter "pin" as AE_Pin GPIO enum.'
        super().__init__(name, description, type_)
        self._pin = pin
        self._initial_state = initial_state

    def _str_details(self):
        return 'pin %s(gpio=%d, conn=%d), value=%s' % (self._pin.name,
                                                       self._pin.value[0], self._pin.value[1],
                                                       self.value())

    def value(self, set_to=None):
        if set_to is not None:
            # Need to change first
            if set_to:
                GPIO.output(self._pin.value[0], GPIO.HIGH)
            else:
                GPIO.output(self._pin.value[0], GPIO.LOW)
        # Now read back the value
        return GPIO.input(self._pin.value[0])

    def setup(self, **kwarg):
        GPIO.setup(self._pin.value[0], GPIO.OUT)
        initial_state = kwarg.get('initial_state', self._initial_state)
        if initial_state is not None:
            GPIO.output(self._pin.value[0], initial_state)

    def on(self):
        return self.value(True)

    def off(self):
        return self.value(False)

    def toggle(self):
        return self.value(not self.value())
