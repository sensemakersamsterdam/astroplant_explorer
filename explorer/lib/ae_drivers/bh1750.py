"""
ae_drivers BH1750 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
#
# Based on code from : Matt Hawkins
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh17580.py
#
# Adapted for Astroplant Explorer framework by: Ted van der Togt
#
from . import _AE_Peripheral_Base
import time
import smbus

I2C_ADDR = 0x23  # default I2C device address
I2C_BUS = 1  # default I2C bus
# Rev 2 Pi, Pi 2, Pi 3, Pi 4 use bus 1
# Rev 1 Pi uses bus 0

def _convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)

class AE_BH1750(_AE_Peripheral_Base):
    """This class is to define a BH1750 type light sensor.
    """

    def __init__(self, name, description, i2c_address=I2C_ADDR, i2c_bus=I2C_BUS):
        super().__init__(name, description, 'BH1750')
        self._addr = i2c_address
        self._bus = smbus.SMBus(i2c_bus)

    def _readLight(self):             
        # Define some constants from the datasheet
        POWER_DOWN = 0x00 # No active state
        POWER_ON   = 0x01 # Power on
        RESET      = 0x07 # Reset data register value
         
        # Start measurement at 4lx resolution. Time typically 16ms.
        CONTINUOUS_LOW_RES_MODE = 0x13
        # Start measurement at 1lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_1 = 0x10
        # Start measurement at 0.5lx resolution. Time typically 120ms
        CONTINUOUS_HIGH_RES_MODE_2 = 0x11
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_1 = 0x20
        # Start measurement at 0.5lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_HIGH_RES_MODE_2 = 0x21
        # Start measurement at 1lx resolution. Time typically 120ms
        # Device is automatically set to Power Down after measurement.
        ONE_TIME_LOW_RES_MODE = 0x23

        bus = self._bus
        addr = self._addr

        data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
        return _convertToNumber(data)
        

    def _str_details(self):
        return 'i2c address %s, values=%s' % (hex(self._addr), str(self.value()))

    def value(self):
        """Read a light value in lux from the sensor
        """
        try:
            return self._readLight()
        except Exception:
            return None

    def setup(self, **kwarg):
        # One throw away reads to get things going...
        self.value()
