"""
Shutdown the Pi if pressed for 5 seconds or longer.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

#
# ToDo: move shutdown code to an utilities module.
#

from ae_drivers.button import AE_Button
from ae_drivers import AE_Pin
from time import sleep
import sys
import os


btn3 = AE_Button('btn3', 'Stop button', AE_Pin.D7)
btn3.setup()

HALT = '/usr/bin/sudo /sbin/shutdown -h --no-wall now'

while True:
    while not btn3.value():
        sleep(0.25)

    print('Shutdown initiated.. ', end='')
    n = 5

    while btn3.value():
        print(n, end=' ')
        sys.stdout.flush()
        n -= 1
        if btn3.last_press_duration() >= 5.0:
            print("Bye bye zwaai zwaai")
            try:
                os.system(HALT)
                sleep(30)  # Wait for the shutdown
            finally:
                print('Error: make sure user is root, this program is setuid root\n',
                      'or sudo for user works without password!')
                sys.exit(-1)
        sleep(1)

    print('\nShutdown aborted...')
