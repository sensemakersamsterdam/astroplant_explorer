"""
ae_drivers Button code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral, GPIO
from time import time


class AE_Button(_AE_Peripheral):
    """Class for a push-button. Buttons should pull signal wire to ground when open.
    """

    def __init__(self, name, description, pin, bouncetime=50,
                 pull_up_down=GPIO.PUD_OFF, inverted=False):
        assert pin.__class__.__name__ == 'AE_Pin' and pin.value[
            2] == 'GPIO', 'Specify parameter "pin" as AE_Pin GPIO enum.'
        assert inverted in [
            True, False], 'Parameter "inverted" should be True or False'
        assert isinstance(bouncetime, int) and 0 <= bouncetime <= 1000, \
            'Parameter "bouncetime" should be 0<= int <= 1000 ms.'
        assert pull_up_down in [GPIO.PUD_OFF, GPIO.PUD_DOWN, GPIO.PUD_UP], \
            'Parameter "pull_up_down" should be one off RPi.GPIO.PUD_*'
        super().__init__(name, description, 'BTN')
        self._pin = pin
        self._pud = pull_up_down
        self._inverted = inverted
        self._bouncetime = bouncetime
        self._pressed = None
        self._last_press_duration = None
        self._last_on_time = None

    def setup(self, **kwargs):
        chan = self._pin.value[0]
        GPIO.setup(chan, GPIO.IN, pull_up_down=self._pud)
        if self.value():
            # Button alreqady on upon initialisation
            self._pressed = 1
            self._last_on_time = time()
        else:
            self._pressed = 0
        GPIO.add_event_detect(
            chan, GPIO.BOTH, self._switch_action, bouncetime=self._bouncetime)

    def value(self):
        """Return current real time state od a button
        """
        v = GPIO.input(self._pin.value[0])
        return not v if self._inverted else v

    def _switch_action(self, channel):
        """Call back to keep state in event thread.
        """
        if self.value():
            self._last_on_time = time()
            self._pressed += 1
        else:
            self._last_press_duration = time() - self._last_on_time

    def pressed_count(self, reset=False):
        n = self._pressed
        if reset:
            self._pressed = 0
        return n

    def last_press_duration(self):
        if self.value():
            # Still pressed
            return time() - self._last_on_time
        else:
            return self._last_press_duration

    def __del__(self):
        try:
            GPIO.remove_event_detect(self._pin.value[0])
        except Exception:
            pass


class AE_Toggle_Button(AE_Button):
    def __init__(self, name, description, pin, **kwargs):
        super().__init__(name, description, pin, **kwargs)
        self.type_ = 'TOGGLE'
        self._toggle = None

    def setup(self, initial=False):
        assert initial in [True, False], \
            'Parameter "initial" should be one True or False'
        chan = self._pin.value[0]
        GPIO.setup(chan, GPIO.IN, pull_up_down=self._pud)
        if self.value():
            # Button already on upon initialisation
            self._last_on_time = time()
            self._toggle = True
        else:
            self._pressed = 0
        self._toggle = initial  # Initial state is determined by the user
        GPIO.add_event_detect(
            chan, GPIO.BOTH, self._toggle_action, bouncetime=self._bouncetime)

    def _toggle_action(self, channel):
        super()._switch_action(channel)
        if self.value():
            self._toggle = not self._toggle

    def state(self):
        return self._toggle
