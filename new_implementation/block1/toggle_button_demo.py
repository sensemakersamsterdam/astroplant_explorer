"""
Demo/test program for the AE_Toggle_Button driver.
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
if True:
    import sys
    sys.path.append('..')
    from ae_drivers import AE_Pin
    from ae_drivers.button import AE_Toggle_Button

tgl1 = AE_Toggle_Button('tgl1', 'Just toggle button 1', AE_Pin.D5)
tgl1.setup()

print('Toggle button demo.')
print('tgl1 prints as %s' % (tgl1))
print('  and its description is:', tgl1.description)

print('\nType Cntl-C to exit and press toggle button 1 a few times...')

try:
    while True:
        print('\nSleeping 5 seconds.')
        sleep(5)
        print('  tgl1.state()=', tgl1.state())
        print('  tgl1.value()=', tgl1.value())
        print('  tgl1.pressed_count()=', tgl1.pressed_count())
        print('  tgl1.last_press_duration()=', tgl1.last_press_duration())
except KeyboardInterrupt:
    print('\nBye bye...')
