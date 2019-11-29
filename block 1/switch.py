"""Script to show how to read switch 1
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function

prev_input = 0

# begin main loop of program
print("\nPress Ctl-C to quit...")
try:
    while True:  # Forever
        input = GPIO.input(AE.SW1)
        if ((not prev_input) and input):
            # Switch is pressed now but not before...
            print("Button pressed")
        prev_input = input                # Remember the before
        sleep(0.05)                       # Wait 50 ms
except KeyboardInterrupt:
    print("Ctl-c has been pressed.")
finally:
    GPIO.cleanup()
