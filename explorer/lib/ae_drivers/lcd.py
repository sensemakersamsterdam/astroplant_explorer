"""
Control the 16x2 LCD display with Hitachi controller.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
# Reworked version from https://raspberrytips.nl/i2c-lcd-scherm/
# (c) portions by Sensemakersams.org and others.
# See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
#

import smbus
from time import sleep
from . import _AE_Peripheral_Base

I2C_ADDR = 0x38  # default I2C device address
I2C_BUS = 1  # default I2C bus on Pi
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE = [
    0x80,  # LCD RAM address for the 1st line
    0xC0  # LCD RAM address for the 2nd line
]

LCD_BACKLIGHT = 0x08

ENABLE = 0b00000100  # Enable bit

E_DELAY = 0.0005

CLEAR_DSP = 0x01  # 000001 Clear display

LCD_INIT = [
    0x33,  # 110011 Initialise
    0x32,  # 110010 Initialise
    0x06,  # 000110 Cursor move direction
    0x0C,  # 001100 Display On,Cursor Off, Blink Off
    0x28   # 101000 Data length, number of lines, font size
]


class AE_LCD(_AE_Peripheral_Base):
    """Class to control the 16x2 LCD display with Hitachi controller.
    """

    def __init__(self, name, description, i2c_address=I2C_ADDR, i2c_bus=I2C_BUS):
        super().__init__(name, description, 'LCD')
        self._addr = i2c_address
        self._bus_number = i2c_bus
        self._n_err = 0
        self.backlight()

    def backlight(self, on=True):
        if on:
            self._backlight = LCD_BACKLIGHT
        else:
            self._backlight = 0

    def setup(self, erase=True):
        self._bus = smbus.SMBus(self._bus_number)
        for cmd in LCD_INIT:
            self._lcd_send(cmd, LCD_CMD)
        if erase:
            self.lcd_clear()

    def _lcd_send(self, bits, mode):

        def strobe(bits):
            # Write with enable high
            addr = self._addr
            self._bus.write_byte(addr, (bits | ENABLE))
            sleep(E_DELAY)  # Time to settle
            self._bus.write_byte(addr, (bits & ~ENABLE))  # strobe in the data
            sleep(E_DELAY)  # Time to capture the data

        try:
            strobe(mode | (bits & 0xF0) | LCD_BACKLIGHT)  # High bits first
            strobe(mode | ((bits << 4) & 0xF0) |
                   LCD_BACKLIGHT)  # Low bits second
        except Exception as ex:
            self._n_err += 1
            if self._n_err == 4:
                print(self.name, ex, '- further errors will be suppressed.')
            elif self._n_err < 4:
                print(self.name, ex)

    def lcd_string(self, message, line):
        assert line == 0 or line == 1, 'Line is 0 or 1.'
        self._lcd_send(LCD_LINE[line], LCD_CMD)
        # right fill message with space and limit to width
        for c in message.ljust(LCD_WIDTH, " ")[:20]:
            self._lcd_send(ord(c), LCD_CHR)

    def lcd_clear(self):
        self._lcd_send(CLEAR_DSP, LCD_CMD)
