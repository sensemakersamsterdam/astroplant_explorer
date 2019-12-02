"""
Demo/test program for the AE_Relay driver.
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
from ae_drivers import AE_Pin, OFF
from ae_drivers.relay import AE_Relay


rly1 = AE_Relay('rly1', 'Fan1 Relay', AE_Pin.D16)
rly1.setup(initial_state=OFF)

print('Relay demo. rly1 prints as:', rly1)
print('and its description is:', rly1.description)

print('\nRelay going on now for 2 seconds...')
rly1.on()
sleep(2)
rly1.off()
print('Done!\n')

print('Relay going on and off rapidly 6 times...')
for _ in range(6):
    rly1.toggle()
    sleep(1)
    print('.', end='', sep='')
    sys.stdout.flush()
print('\nDone!\n')

rly1.off()  # make sure we start off...
print('And now we read status for the relay when off...')
print('Relay is_on() gives:', rly1.is_on())
print('Relay is_off() gives:', rly1.is_off())
print('Relay value() gives:', rly1.value())
sleep(2)

print('\nAnd now we toggle the relay with toggle() and read its status again.')
rly1.toggle()
print('Relay is_on() now gives:', rly1.is_on())
print('Relay is_off() now gives:', rly1.is_off())
print('Relay value() now gives:', rly1.value())
sleep(2)

rly1.off()
print('\nDemo ended. Relay should be off.')
