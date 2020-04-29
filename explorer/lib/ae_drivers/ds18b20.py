"""
ae_drivers DD18B20 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
#
# Based on code from ...
#
# Adapted for Astroplant Explorer framework by: Ted van der Togt
#
from . import _AE_Peripheral_Base
import time
import os
import glob

DEBUG = 1  # Normally on 0. Non zero enable debug code/exceptions

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

class AE_DS18B20(_AE_Peripheral_Base):
    """This class is to define a DS18B20 type (water)temperature sensor.
    """

    def __init__(self, name, description):
        super().__init__(name, description, 'DS18B20')
        
    def _read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_temp(self):
        lines = _read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = _read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            #temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
        

    def _str_details(self):
        return 'values=%s' % (str(self.value()))

    def value(self):
        """Read a temperature value in Celsius from the sensor
        """
        try:
            return self._read_temp()
        except Exception as ex:
            if DEBUG:
                raise ex
            return None

    def setup(self, **kwarg):
        # One throw away reads to get things going...
        self.value()
