"""
Demo/test program for the AE_Buzzer driver.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Ted van der Togt
# Adapted from AE_Relay by: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from time import sleep
import sys
from ae_drivers import AE_Pin, OFF
from ae_drivers.buzzer import AE_Buzzer


buz1 = AE_Buzzer('buz1', 'Simple piezo buzzer', AE_Pin.D19)
buz1.setup(initial_state=OFF)

print('Buzzer demo. buz1 prints as:', buz1)
print('and its description is:', buz1.description)

print('\nBuzzer now buzzing for 1 second...')
buz1.on()
sleep(1)
buz1.off()
print('Done!\n')

buz1.off()
print('\nDemo ended. Buzzer should be silent.')
