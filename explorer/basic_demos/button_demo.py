"""
Demo/test program for the AE_Button driver.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

# This program shows some features of the Button library class

# From the standard time library we only require sleep()
from time import sleep
# And we need the definitions of our pins
from ae_drivers import AE_Pin
# And we need the Button driver class
from ae_drivers.button import AE_Button

# Then we define and initialize Button 1
btn1 = AE_Button('btn1', 'Just button 1', AE_Pin.D5)
btn1.setup()

# And Button 2
btn2 = AE_Button('btn2', 'Just button 2', AE_Pin.D6)
btn2.setup()

# And 3
# For this button we reverse the action. Use if your button reports open
# as closed vv
btn3 = AE_Button('btn3', 'Just button 3', AE_Pin.D7, inverted=True)
btn3.setup()

print('Button demo.')
# Now demo some of the info features for all three buttons
print('btn1 prints as %s' % (btn1))
print('  and its long description is:', btn1.description)
print('btn2 prints as %s' % (btn2))
print('  and its long description is:', btn2.description)
print('btn3 prints as %s' % (btn3))
print('  and its long description is:', btn3.description)

print('\nType Cntl-C to exit this demo.')
print('Now press (and sometmes hold) buttons 1-3 a few times...')

try:
    while True:
        print('\nSleeping a while. Use your buttons.')
        sleep(8)
        print('Now checking yout buttons...')

        # Cycle through all three of them.
        # Each time through the loop btn acts as one of the buttons from the list.
        # Way more elegant as the straight repetition of code a bit above where we printed
        # out the button's description.
        for btn in [btn1, btn2, btn3]:
            print('  %s value()=%s.', (btn.name, btn.value()))
            print('  %s pressed_count()=%s.',
                  (btn.name, btn.pressed_count()))
            print('  %s last_press_duration()=%s',
                  (btn.name, btn.last_press_duration()))

except KeyboardInterrupt:
    print('\nBye bye...')
