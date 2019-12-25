"""
Demo/test program for listening for MQTT messages to show on LCD.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.
import sys
from time import sleep
from ae_util.configuration import cfg
from ae_util.mqtt import AE_Local_MQTT
from ae_drivers.lcd import AE_LCD

# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

# Define the display
lcd = AE_LCD('lcd', '16x2 LCD display')
# And initialize it without erasing.
lcd.setup(erase=False)

stop = False

# Call back 1 to handle button events
def cb1(sub_topic, payload, rec_time):
    print('call_back 1:', sub_topic, payload, rec_time)
    if payload == 'True':
        print ('button toggle on')
        lcd.lcd_string('lights on', 0)
    elif payload == 'False':
        print ('button toggle off')
        lcd.lcd_string('lights off', 0)
    else:
        print ('unspecified payload...')
        lcd.lcd_string('dont know what to do', 0)

# Call back 2 to handle DHT readings
def cb2(sub_topic, payload, rec_time):
    print('call_back 2:', sub_topic, payload, rec_time)
    lcd.lcd_string(payload, 0)

# Special call back to stop the listener
def cb_stop(sub_topic, payload, rec_time):
    global stop
    print('Received stop request. mqtt_lcd_receiver bailing out!')
    lcd.lcd_string('bye bye', 0)
    sleep(1)
    stop = True

# This lcd receiver listens to topics 'button1' 'dht22' and 'control'
loc_mqtt.subscribe('button1/#', cb1)
loc_mqtt.subscribe('dht22/#', cb2)
loc_mqtt.subscribe('control/stop', cb_stop)

print('Abort with control-c to end prematurely.')
try:
    while not stop:
        sub_topic, payload, rec_time = loc_mqtt.get_message()
        if sub_topic is not None:
            print('Dequeued:', sub_topic, payload, rec_time)
        sleep(0.1)
except KeyboardInterrupt:
    print('\nManually aborted....\nBye bye')
