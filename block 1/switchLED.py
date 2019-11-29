"""Script to show how to switch LED1 with SW1.
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function

prev_input = 0

# Start with led OFF
led_state = 0
GPIO.output(AE.LED1, GPIO.LOW)


def toggle_led():
    global led_state
    if (LED_state):
        # Led is ON -> Switch it OFF
        GPIO.output(AE.LED1, GPIO.LOW)
        led_state = 0
    else:
        # Led is ON -> Switch it OFF
        GPIO.output(AE.LED1, GPIO.HIGH)
        led_state = 1


# begin main loop of program
print("\nPress Ctl-C to quit...")
try:
    while True:  # Forever
        input = GPIO.input(AE.SW1)
        if ((not prev_input) and input):
            # Switch is pressed now but not before...
            print("Button pressed")
            toggle_led()

        prev_input = input
        sleep(0.05)
except KeyboardInterrupt:
    print("Ctl-c has been pressed.")
finally:
    GPIO.output(AE.LED1, GPIO.LOW)  # LED1 to off
    GPIO.cleanup()
