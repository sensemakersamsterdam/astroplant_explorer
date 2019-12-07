import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(5, GPIO.IN)
prev_input = 0
LED_state = 0
while True:
    input = GPIO.input(5)
    if ((not prev_input) and input):
        print("Button pressed")
        LED_state = not LED_state
        if (LED_state):
            GPIO.output(20, GPIO.HIGH)
        else:
            GPIO.output(20, GPIO.LOW)
    prev_input = input
    time.sleep(0.05)
