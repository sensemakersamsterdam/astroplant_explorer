"""
ae_drivers actuators common code. Provides most of the implementation for simple LEDs, Relays etc.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral, GPIO, ON, OFF


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
        """Return the current value of the actuator if there is no parameter, else
           set it first to the value given and then return the current state.
        """
        if set_to is not None:
            # Need to change state first
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
        return self.value(ON)

    def off(self):
        return self.value(OFF)

    def toggle(self):
        return self.value(not self.value())
