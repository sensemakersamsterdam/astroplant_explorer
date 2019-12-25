"""
Demo/test program for the MQTT utilities.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from ae_util.configuration import cfg
from ae_util.mqtt import AE_Local_MQTT
from ae_drivers import AE_Pin
from ae_drivers.led import AE_LED
from time import sleep
import sys
#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

led = AE_LED('led', 'The red LED', AE_Pin.D20)
led.setup()

stop = False


def cb1(sub_topic, payload, rec_time):
    print('call_back 1:', sub_topic, payload, rec_time)
    if sub_topic == 'button1' and payload == 'True':
        print ('led on')
        led.value(1) 
    elif sub_topic == 'button1' and payload == 'False':
        print ('led off')
        led.value(0)
    else:
        print ('not for me...')

def cb_stop(sub_topic, payload, rec_time):
    global stop
    print('Received stop request. mqtt_receiver_demo bailing out!')
    stop = True

# This led receiver listens to topic 'button1'
loc_mqtt.subscribe('button1/#', cb1)

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
