"""Shutdown the Pi if pressed for 5 seconds or longer.
"""
from time import sleep
import os
if True:
    import sys
    sys.path.append('..')
    from ae_drivers import AE_Pin
    from ae_drivers.button import AE_Button


btn3 = AE_Button('btn3', 'Stop button', AE_Pin.D7)
btn3.setup()

HALT = 'sudo shutdown -h --no-wall now'

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
                print('Error: make sure shutdown is in the path and user',
                      'is setuid root or can sudo without password!')
                sys.exit(-1)
        sleep(1)

    print('\nShutdown aborted...')
