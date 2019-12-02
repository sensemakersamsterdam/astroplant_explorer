"""
Demo/test program for the AE_Toggle_Button and AE_LED drivers.
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
    from ae_drivers.led import AE_LED

tgl1 = AE_Toggle_Button('btn1', 'Just toggle button 1', AE_Pin.D5)
tgl1.setup()

led3 = AE_LED('led3', 'The red LED', AE_Pin.D20)
led3.setup()

led4 = AE_LED('led4', 'The blue LED', AE_Pin.D21)
led4.setup()

print('LED4 follows the button 1 and LED3 is toggled on and off.')
print('\nType Cntl-C to exit and press button 1 a few times...')

try:
    while True:
        led3.value(tgl1.state())  # Copy toggle state of button 1 to LED 3
        led4.value(tgl1.value())  # Copy button state of button 1 to LED 4
        sleep(0.1)   # Delay a bit  
except KeyboardInterrupt:
    print('\nBye bye...')
