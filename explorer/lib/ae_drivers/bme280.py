"""
ae_drivers BME280 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
#
# Official datasheet available from :
# https://www.bosch-sensortec.com/bst/products/all_products/bme280
#
# Based on code from : Matt Hawkins
# Date   : 21/01/2018
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py
#
# Adapted for Astroplant Explorer framework by: Ted van der Togt, Gijs Mos
#
from . import _AE_Peripheral_Base
import time
import smbus

DEBUG = 0  # Normally on 0. Non zero enable debug code/exceptions

I2C_ADDR = 0x76  # default I2C device address
I2C_BUS = 1  # default I2C bus
# Rev 2 Pi, Pi 2, Pi 3, Pi 4 use bus 1
# Rev 1 Pi uses bus 0


def _getShort(data, index):
    # return two bytes from data at position index as a 16-bit value
    result = _getUShort(data, index)
    return result if result < 32767 else result - 65536


def _getUShort(data, index):
    # return two bytes from data as an unsigned 16-bit value
    return (data[index+1] << 8) + data[index]


def _getChar(data, index):
    # return one byte from data as an signed 8-bit value
    result = data[index]
    return result if result < 127 else result - 256


def _getUChar(data, index):
    # return one byte from data as an unsigned char
    return data[index] & 0xFF


class AE_BME280(_AE_Peripheral_Base):
    """This class is to define a BME280 type temperature/pressure/humidity sensor.
    """
    _instance = None

    def __new__(cls, *_pars, **_kpars):
        # We implement as singleton class
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name, description, i2c=None, i2c_address=I2C_ADDR, i2c_bus=I2C_BUS):
        if i2c is not None:
            bus = i2c
        else:
            bus = smbus.SMBus(i2c_bus)
        if not hasattr(self, 'name'):
            # First init of the singleton
            super().__init__(name, description, 'BME280')
            self._addr = i2c_address
            self._i2c = bus
        else:
            # Subsequent one
            if name != self.name or \
                    description != self.description or \
                    self._addr != i2c_address:
                print("Subsequent __init__ of singleton AE_BME280 ignored.")

    def _readBME280All(self):
        # Register Addresses
        REG_DATA = 0xF7
        REG_CONTROL = 0xF4
        # REG_CONFIG = 0xF5

        REG_CONTROL_HUM = 0xF2
        # REG_HUM_MSB = 0xFD
        # REG_HUM_LSB = 0xFE

        # Oversample setting - page 27
        OVERSAMPLE_TEMP = 2
        OVERSAMPLE_PRES = 2
        MODE = 1

        bus = self._i2c
        addr = self._addr

        # Oversample setting for humidity register - page 26
        OVERSAMPLE_HUM = 2
        bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

        control = OVERSAMPLE_TEMP << 5 | OVERSAMPLE_PRES << 2 | MODE
        bus.write_byte_data(addr, REG_CONTROL, control)

        # Read blocks of calibration data from EEPROM
        # See Page 22 data sheet
        cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
        cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
        cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

        # Convert byte data to word values
        dig_T1 = _getUShort(cal1, 0)
        dig_T2 = _getShort(cal1, 2)
        dig_T3 = _getShort(cal1, 4)

        dig_P1 = _getUShort(cal1, 6)
        dig_P2 = _getShort(cal1, 8)
        dig_P3 = _getShort(cal1, 10)
        dig_P4 = _getShort(cal1, 12)
        dig_P5 = _getShort(cal1, 14)
        dig_P6 = _getShort(cal1, 16)
        dig_P7 = _getShort(cal1, 18)
        dig_P8 = _getShort(cal1, 20)
        dig_P9 = _getShort(cal1, 22)

        dig_H1 = _getUChar(cal2, 0)
        dig_H2 = _getShort(cal3, 0)
        dig_H3 = _getUChar(cal3, 2)

        dig_H4 = _getChar(cal3, 3)
        dig_H4 = (dig_H4 << 24) >> 20
        dig_H4 = dig_H4 | (_getChar(cal3, 4) & 0x0F)

        dig_H5 = _getChar(cal3, 5)
        dig_H5 = (dig_H5 << 24) >> 20
        dig_H5 = dig_H5 | (_getUChar(cal3, 4) >> 4 & 0x0F)

        dig_H6 = _getChar(cal3, 6)

        # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
        wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + \
            ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
        time.sleep(wait_time/1000)  # Wait the required time

        # Read temperature/pressure/humidity
        data = bus.read_i2c_block_data(addr, REG_DATA, 8)
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw = (data[6] << 8) | data[7]

        # Refine temperature
        var1 = ((((temp_raw >> 3)-(dig_T1 << 1)))*(dig_T2)) >> 11
        var2 = (((((temp_raw >> 4) - (dig_T1)) *
                  ((temp_raw >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
        t_fine = var1+var2
        temperature = float(((t_fine * 5) + 128) >> 8)

        # Refine pressure and adjust for temperature
        var1 = t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * dig_P6 / 32768.0
        var2 = var2 + var1 * dig_P5 * 2.0
        var2 = var2 / 4.0 + dig_P4 * 65536.0
        var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * dig_P1
        if var1 == 0:
            pressure = 0
        else:
            pressure = 1048576.0 - pres_raw
            pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
            var1 = dig_P9 * pressure * pressure / 2147483648.0
            var2 = pressure * dig_P8 / 32768.0
            pressure = pressure + (var1 + var2 + dig_P7) / 16.0

        # Refine humidity
        humidity = t_fine - 76800.0
        humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * \
            (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 *
                                 humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
        humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
        if humidity > 100:
            humidity = 100.0
        elif humidity < 0:
            humidity = 0.0

        return (round(temperature/100.0, 1), round(pressure/100.0, 1), round(humidity, 1))

    def _str_details(self):
        return 'i2c address %s, values=%s' % (hex(self._addr), str(self.values()))

    def values(self):
        try:
            return self._readBME280All()
        except Exception as ex:
            if DEBUG:
                raise ex
            return (None, None, None)

    def setup(self, **kwarg):
        # One throw away reads to get things going...
        # Also test if we actually have a sensor
        try:
            self._readBME280All()
        except Exception as ex:
            print('Cannot read BME280. Is sensor connected? Message: %s' % ex)
