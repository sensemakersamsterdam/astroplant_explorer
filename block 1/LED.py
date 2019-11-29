"""Simple script to switch LED1 on for one second.
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function

print("LED1 on")
GPIO.output(AE.LED1, GPIO.HIGH)     # LED1 is on now
sleep(1)                            # Wait a second
print("LED1 off")
GPIO.output(AE.LED1, GPIO.LOW)      # LED1 is off again
