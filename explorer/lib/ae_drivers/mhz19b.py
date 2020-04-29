"""
ae_drivers MH-Z19B CO2 sensor code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Documentation in Japanese and English:
# http://qiita.com/UedaTakeyuki/items/c5226960a7328155635f
# https://www.winsen-sensor.com/d/files/infrared-gas-sensor/mh-z19b-co2-ver1_0.pdf

# Import base class for all sensors and the seial class to read from the device
from . import _AE_Peripheral_Base
import serial

# START_BYTE + SENSOR# + READ_CO2 + PADDING + CHECHSUM
_COMMAND = b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'


class AE_MHZ19B(_AE_Peripheral_Base):
    """Class to control a MH-Z19B CO2 sensor
    """

    def __init__(self, name, description,
                 device='/dev/serial0',
                 baudrate=9600,
                 bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE):
        """Setup peripheral base and the communication device
        """
        super().__init__(name, description, 'CO2 Sensor')
        self._device = device
        self._serial = serial.Serial(device,
                                     baudrate=baudrate,
                                     bytesize=bytesize,
                                     parity=parity,
                                     stopbits=stopbits,
                                     timeout=1.0)

    def value(self):
        """Read a CO2 value from the sensor
        """
        try:
            self._serial.write(_COMMAND)
            s = self._serial.read(9)
            if s[0] == 0xff and s[1] == 0x86:
                # We did get a CO2 reading
                return s[2]*256 + s[3]
        except Exception:
            # Time-out, bad data, whatever
            pass
        return None

    def _str_details(self):
        """Some more default into the __str__ dunder form the base class
        """
        return 'device=%s, value=%s ppm' % (self._device,
                                            self.value())

    def setup(self):
        pass

    def __del__(self):
        self._serial.close()
        self._serial = None
