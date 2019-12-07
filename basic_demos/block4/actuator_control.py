# this is a basic version, timing of LEDs still hard coded in this script...
# for explanation of time functions see https://docs.python.org/3/library/time.…
# this script uses time in minutes: every day has 24 x 60 = 1440 minutes 
# every minute, the specified conditions are evaluated and lighting changed if neccessary

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT) #fan 1 for cooling the astroplant
GPIO.setup(18, GPIO.OUT) #farred (or green)
GPIO.setup(19, GPIO.OUT) #fan 2 for CO2 sensor
GPIO.setup(20, GPIO.OUT) #red
GPIO.setup(21, GPIO.OUT) #blue
GPIO.output(16, GPIO.HIGH) #fan 1 is always on
GPIO.output(19, GPIO.HIGH) #fan 2 is always on
pwm_farred = GPIO.PWM(18, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_red = GPIO.PWM(20, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_blue = GPIO.PWM(21, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_farred.start(0)
pwm_red.start(0)
pwm_blue.start(0)

def red(t):
    if 0<= t <360:
        return (0)
    elif 360<= t < 1320:
        return (100)
    else:
        return (0)

def blue(t):
    if 0<= t <360:
        return (0)
    elif 720<= t < 1320:
        return (100)
    else:
        return (0)
    
def farred(t):
    if 0<= t <360:
        return (0)
    elif 360<= t < 1080:
        return (100)
    else:
        return (0)

while True:
    tmin= (time.localtime()[3] * 60 + time.localtime()[4]) #actual time in minutes of the day
    pwm_farred.ChangeDutyCycle(farred(tmin))
    pwm_red.ChangeDutyCycle(red(tmin))
    pwm_blue.ChangeDutyCycle(blue(tmin))
    print("At "+str(tmin//60)+":"+ str(tmin % 60)+" red is set to "+str(red(tmin))+ "%, blue to "+str(blue(tmin))+ "% and farred to "+str(farred(tmin))+ "%")
    time.sleep(60)