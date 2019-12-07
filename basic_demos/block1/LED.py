import RPi.GPIO as GPIO #import the library to control the GPIO pins
import time
#settings for GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.OUT)#connect the led to GPIO pin 20

print("LED on")
GPIO.output(20, GPIO.HIGH) #turn the LED on
time.sleep(1)
print("LED off")
GPIO.output(20, GPIO.LOW) #turn the LED off
