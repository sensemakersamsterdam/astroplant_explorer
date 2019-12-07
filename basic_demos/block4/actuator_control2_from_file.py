# this script controls fans and LEDs of the AstroPlant Explorer
# in future it could be adapted to read a light recipe from an external json file

import RPi.GPIO as GPIO
import json
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)  # fan 1 for cooling the astroplant
GPIO.setup(18, GPIO.OUT)  # farred (or green)
GPIO.setup(19, GPIO.OUT)  # fan 2 for CO2 sensor
GPIO.setup(20, GPIO.OUT)  # red
GPIO.setup(21, GPIO.OUT)  # blue
GPIO.output(16, GPIO.HIGH)  # fan 1 is always on
GPIO.output(19, GPIO.HIGH)  # fan 2 is always on
pwm_farred = GPIO.PWM(18, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_red = GPIO.PWM(20, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_blue = GPIO.PWM(21, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm_farred.start(0)
pwm_red.start(0)
pwm_blue.start(0)

with open('recipe1.json') as f:
    recipe = json.load(f)
# print(recipe)


def makeList(colour):
    if colour in recipe:
        clr = recipe[colour]
        clr_list = []
        for element in clr:
            # interpret as timenotation
            time_obj = time.strptime(element['time'], '%H:%M')
            time_min = time_obj[3]*60 + time_obj[4]  # convert to minutes
            # convert to list pair
            clr_list.append((time_min, element['value']))
        clr_list.sort()  # make sure list is sorted
        if clr_list[0][0] > 0:  # fill value for first interval from 00:00 to first event with value of that for the interval after last event
            last_value = clr_list[len(clr_list) - 1][1]
            clr_list.insert(0, (0, last_value))
        return(clr_list)
    else:
        return([(0, 0)])


def led_val(list, t):
    list.sort()
    templist = []
    for i in list:
        templist.append(i[0])
    if t in templist:
        i = templist.index(t)
        return(list[i][1])
    else:
        templist.append(t)
        templist.sort()
        i = templist.index(t)
        return(list[i-1][1])


red_list = makeList("red")
blue_list = makeList("blue")
farred_list = makeList("farred")
print((red_list), (blue_list), farred_list)

while True:
    # actual time in minutes of the day
    tmin = (time.localtime()[3] * 60 + time.localtime()[4])
    pwm_farred.ChangeDutyCycle(led_val(farred_list, tmin))
    pwm_red.ChangeDutyCycle(led_val(red_list, tmin))
    pwm_blue.ChangeDutyCycle(led_val(blue_list, tmin))
    #print("At t = "+str(tmin//60)+":"+ str(tmin % 60)+" red is set to "+str(led_val(red_list, tmin))+ "%, blue to "+str(led_val(blue_list, tmin))+ "% and farred to "+str(led_val(farred_list, tmin))+ "%")
    time.sleep(60)
