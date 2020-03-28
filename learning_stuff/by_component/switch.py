import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN)
prev_input = 0
while True:
    input = GPIO.input(7)
    if ((not prev_input) and input):
        print("Button pressed")
    prev_input = input
    time.sleep(0.05)
