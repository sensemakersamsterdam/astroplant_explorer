# relay script. Zet een standaard relais aan en uit, op dezelfde manier als een LED.
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)

GPIO.output(16, GPIO.HIGH)
print("relay on")
time.sleep(3)
GPIO.output(16, GPIO.LOW)
print("relay off")
