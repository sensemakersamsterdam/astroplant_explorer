"""Shows how to switch on a LED for 1 second.
"""

import RPi.GPIO as GPIO  # import the library to control the GPIO pins
import time

# settings for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# connect the led to GPIO pin 20
GPIO.setup(20, GPIO.OUT)

print("LED on")
GPIO.output(20, GPIO.HIGH)  # turn the LED on

# Wait a second
time.sleep(1)

print("LED off")
GPIO.output(20, GPIO.LOW)  # turn the LED off
