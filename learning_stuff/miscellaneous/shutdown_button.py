# This script turns off the Pi when pushing button 3 (on pin D7) longer than 5 s.
import RPi.GPIO as GPIO
import os
import time

gpio_pin_number = 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
    time.sleep(5)
    print("Bye bye zwaai zwaai")
    os.system("sudo shutdown -h now")
except:
    pass

GPIO.cleanup()
