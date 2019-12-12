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

# Shutdown the Pi when Button 3 is pressed 5 seconds.

# First get and initialize the button driver library
from ae_drivers.button import AE_Button
# And get the Pin definitions from the library.
from ae_drivers import AE_Pin
# From the time library we only need sleep.
from time import sleep
# And we need the sys and os libraries too.
import sys
import os

# Now define the button we will use.
btn3 = AE_Button('btn3', 'Stop button', AE_Pin.D7)
# And initialize the hardware it is connected to.
btn3.setup()

# This is the Linux command that will shut down our Pi.
HALT = '/usr/bin/sudo /sbin/shutdown -h --no-wall now'

# We will repeat this forever untill we die.
while True:
    # FIrst we'll wait for the button to be pressed
    while not btn3.value():
        # Not pressed. Let's check again in a quarter of a sec.
        # You do not really need the sleep, but is is friendlier
        # since it will give te CPU to other programs more.
        sleep(0.25)

    # Now, let the user know that we have started to count down.
    # By the way, the "end=''" suppresses the newline from the print.
    print('Shutdown initiated.. ', end='')
    n = 5

    while btn3.value():
        # Button is still pressed.
        # Print the second down counter.
        print(n, end=' ')
        # And tell Python to flush it to the console immediately.
        # If you want to know more, read about "I/O buffering".
        sys.stdout.flush()
        n -= 1
        # Now ask the button how long ago it was pressed.
        if btn3.last_press_duration() >= 5.0:
            # More than 5 secs ago. Make us and the rest of the Pi die!
            # Print our last will and testament.
            print("Bye bye zwaai zwaai")
            try:
                os.system(HALT)
                sleep(30)  # Wait for the shutdown to happen.
            finally:
                # We will only get here if the shutdown failed somehow.
                # This means that your PI was not set-up properly.
                # SO we just print an error message and exit.
                print('Error: make sure user is root, this program is setuid root\n',
                      'or sudo for user works without password!')
                sys.exit(-1)
        # No time to die yet, so wait a second before we print the next countdown. 
        sleep(1)

    # Chickened out. Button was released. So let it be known to the world
    # and continue running the outer loop waiting for the next press. 
    print('\nShutdown aborted...')
