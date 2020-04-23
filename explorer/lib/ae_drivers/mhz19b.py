"""
ae_drivers MH-Z19B CO2 sensor code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Addapted from:
# http://eleparts.co.kr/data/design/product_file/SENSOR/gas/MH-Z19_CO2%20Manual%20V2.pdf
# http://qiita.com/UedaTakeyuki/items/c5226960a7328155635f

from . import _AE_Peripheral_Base
import serial

COMMAND = b'\xff\x01\x86\x00\x00\x00\x00\x00\x79'


class AE_MHZ19B(_AE_Peripheral_Base):
    """Class to control a MH-Z19B CO2 sensor
    """

    def __init__(self, name, description,
                 device='/dev/ttyS0',
                 baudrate=9600,
                 bytesize=serial.EIGHTBITS,
                 parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE):
        super().__init__(name, description, 'CO2')
        self._device = device
        self._serial = serial.Serial(device,
                                     baudrate=baudrate,
                                     bytesize=bytesize,
                                     parity=parity,
                                     stopbits=stopbits,
                                     timeout=1.0)

    def value(self):
        try:
            self._serial.write(COMMAND)
            s = self._serial.read(9)
            if s is None:
                return None
        except Exception:
            return None

        if s[0] == "\xff" and s[1] == "\x86":
            return (ord(s[2])*256 + ord(s[3]))

    def _str_details(self):
        return 'device = %s, value = %s' % (self._device,
                                            self.value())

    def setup(self):
        pass
