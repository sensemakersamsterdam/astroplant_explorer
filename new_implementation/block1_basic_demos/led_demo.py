"""
Demo/test program for the AE_LED driver.
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
import sys
from ae_drivers.led import AE_LED
from ae_drivers import AE_Pin, OFF

led1 = AE_LED('led1', 'Super bright red LED', AE_Pin.D20)
led1.setup(initial_state=OFF)

print('LED demo. led1 prints as:', led1)
print('and its description is:', led1.description)

print('\nLED going on now for 2 seconds...')
led1.on()
sleep(2)
led1.off()
print('Done!\n')

print('LED going on and off rapidly 20 times...')
for _ in range(20):
    led1.toggle()
    sleep(0.2)
    print('.', end='')
    sys.stdout.flush()
print('\nDone!\n')

led1.off()  # make sure we start off...
print('And now we read status for the LED when off...')
print('LED is_on() gives:', led1.is_on())
print('LED is_off() gives:', led1.is_off())
print('LED value() gives:', led1.value())
sleep(2)

print('\nAnd now we toggle the led with toggle() and read its status again.')
led1.toggle()
print('LED is_on() now gives:', led1.is_on())
print('LED is_off() now gives:', led1.is_off())
print('LED value() now gives:', led1.value())
sleep(2)

led1.off()
print('\nDemo ended. Led should be off.')
