"""
Demo/test program for the MQTT utilities.
See https://github.com/sensemakersamsterdam/astroplant_explorer 
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Ted van der Togt
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.
# 
from ae_util.configuration import cfg
from ae_util.mqtt import AE_Local_MQTT
import json
import time

# read light recipe
with open('light_recipe.json') as f:
    recipe = json.load(f)
    #print(recipe) #for debugging

# help function to make list for a given colour with time:value pairs (time expressed as minute of the day) 
def makeList(colour):
    if colour in recipe:
        clr = recipe[colour]
        clr_list = []
        for element in clr:
            # interpret as timenotation
            time_obj = time.strptime(element['time'], '%H:%M')
            time_min = time_obj[3]*60 + time_obj[4]  # convert times to minutes in day
            # convert to list pair
            clr_list.append([time_min, element['value']])
        clr_list.sort()  # make sure list is sorted
        if clr_list[0][0] > 0:  # fill value for first interval from 00:00 to first event with value of that for the interval after last event
            last_value = clr_list[-1][1]
            clr_list.insert(0, [0, last_value])
        return(clr_list)
    else:
        return([(0, 0)])

# helpfunction to find led value from list at time t ( t expressed as minute of the day)
def led_val(list, t):
    for i in range(len(list)):
        if list[i][0] > t:
            return(list[i-1][1])
    if t<1440:
        return(list[-1][1])
    
red_list = makeList("red")
blue_list = makeList("blue")
farred_list = makeList("farred")
#print((red_list), (blue_list), farred_list) # for debugging

red_value=0
blue_value=0
farred_value=0

#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()
# 
print('\nType Cntl-C to exit and press button 1...')
print('Scheduled LED values over MQTT demo.')
print('values published under topic: led_values and subtopic: red_value, blue_value, farred_value' )

try:
    while True:
        # actual time expressed as minute of the day
        tm = (time.localtime()[3] * 60 + time.localtime()[4])
        print(tm)
        if red_value != led_val(red_list, tm):
            red_value = led_val(red_list, tm)
            #print(red_value)
            print('sub-topic: led_values/red', loc_mqtt.publish('led_values/red', red_value))
        if blue_value != led_val(blue_list, tm):
            blue_value = led_val(blue_list, tm)
            print('sub-topic: led_values/blue', loc_mqtt.publish('led_values/blue', blue_value))
        if farred_value != led_val(farred_list, tm):
            farred_value = led_val(farred_list, tm)
            print('sub-topic: led_values/farred', loc_mqtt.publish('led_values/farred', farred_value))   
        time.sleep(60) #wait a minute
except KeyboardInterrupt:
    print('\nBye bye...')

