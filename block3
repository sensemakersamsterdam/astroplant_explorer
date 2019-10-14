#relay script block 3
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
print("relay on")
GPIO.output(16, GPIO.HIGH)
time.sleep(1)
print("relay off")
GPIO.output(16, GPIO.LOW)
