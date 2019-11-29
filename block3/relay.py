"""Script to switch a relay on and off. Similar to the LED switch from block 1.
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function

GPIO.output(AE.RY1, GPIO.HIGH)
print("relay 1 on")
sleep(3)
GPIO.output(AE.RY1, GPIO.LOW)
print("relay  1 off")
GPIO.cleanup()
