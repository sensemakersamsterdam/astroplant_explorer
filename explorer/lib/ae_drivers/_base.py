"""
ae_drivers base code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

import sys
import RPi.GPIO as GPIO
from enum import Enum

if sys.version_info.major < 3 or sys.version_info.minor < 5:
    raise NotImplementedError('This software is not implemented for Python versions before 3.5')

# We will use the GPIO module in BCM mode. So we pass GPIO numbers to
# the library.  Also we do not want warnings printed.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Just for convenience an ON and OFF constant.
ON = 1
OFF = 0

# Here are the pin numbers we use. They are an Enum of tuples.
# First member is the GPIO number.
# Second member is the physical pin number on the connector.
# 3rd parameter is interface type. Try help(AE_Pin) from Python.


class AE_Pin(Enum):
    """Enum for Astroplant Explorer peripheral pins.
    Specifies the name as used in the code, the BCM GPIO pin number, the physical pin number and
    how the pin is used in the Astroplant Explorer code.
    """
    ONE_WIRE = (4, 7, 'onewire')
    UART_Rx = (15, 10, 'serial')
    UART_Tx = (14, 8, 'serial')
    I2C_SCL = (3, 5, 'I2C')
    I2C_SDA = (2, 3, 'I2C')
    DHT = (17, 11, 'DHT')
    D5 = (5, 29, 'GPIO')
    D6 = (6, 31, 'GPIO')
    D7 = (7, 26, 'GPIO')
    D16 = (16, 36, 'GPIO')
    D18 = (18, 12, 'GPIO')
    D19 = (19, 35, 'GPIO')
    D20 = (20, 38, 'GPIO')
    D21 = (21, 40, 'GPIO')


class _AE_Peripheral_Base:
    """Base class for the Astroplant Explorer peripherals. Defines a name and a description,
    """

    def __init__(self, name, description, type_):
        assert isinstance(name, str) and len(
            name) > 0, 'Parameter "name" should be non-empty string.'
        assert isinstance(description, str) and len(
            description) > 0, 'Parameter "description" should be non-empty string.'
        self.name = name    # Short name
        self.description = description  # Longer description
        self.type_ = type_

    def _str_details(self):
        return ''

    def __str__(self):
        return '<%s %s %s>' % (self.type_, self.name,
                               self._str_details())


class _AE_Peripheral(_AE_Peripheral_Base):
    """Base class for most Astroplant Explorer peripherals. Defines some basic methods.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def value(self, set_to=None):
        raise NotImplementedError

    def setup(self, **kwarg):
        raise NotImplementedError

    def is_on(self):
        return self.value() == ON

    def is_off(self):
        return self.value() == OFF

    def __str__(self):
        return '<%s %s is %s %s>' % (self.type_, self.name,
                                     'ON' if self.is_on() else 'OFF',
                                     self._str_details())
