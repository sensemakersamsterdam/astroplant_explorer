"""
Demo/test program for the AE_Button and AE_LED drivers.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from time import sleep
from ae_drivers import AE_Pin
from ae_drivers.button import AE_Button
from ae_drivers.led import AE_LED

btn1 = AE_Button('btn1', 'Just button 1', AE_Pin.D5)
btn1.setup()

led3 = AE_LED('led3', 'The red LED', AE_Pin.D20)
led3.setup()


print('\nType Cntl-C to exit and press button 1...')

try:
    while True:
        led3.value(btn1.value())  # Copy value of button 1 to LED 3
        sleep(0.1)   # Delay a bit
except KeyboardInterrupt:
    print('\nBye bye...')
