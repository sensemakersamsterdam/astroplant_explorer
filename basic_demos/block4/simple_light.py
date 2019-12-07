# this is a first concept; 
# this script uses time in minutes: every day has 24 x 60 = 1440 minutes 
# a while loop generates a time (with 25 min in between) and sets the light accordingly

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) #farred (or green)
GPIO.setup(20, GPIO.OUT) #red
GPIO.setup(21, GPIO.OUT) # blue
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

def setLight(t):
    pwm_farred.ChangeDutyCycle(farred(t))
    pwm_red.ChangeDutyCycle(red(t))
    pwm_blue.ChangeDutyCycle(blue(t))
    print("On "+str(n//60)+":"+ str(n % 60)+" red is set to "+str(red(t))+ "%, blue to "+str(blue(t))+ "% and farred to "+str(farred(t))+ "%")

for n in range (0, 1439, 25):
    setLight(n)
    time.sleep(1)
