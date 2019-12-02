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
from time import sleep
from ae_util.mqtt import AE_Local_MQTT
import sys

#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

stop = False


def cb1(sub_topic, payload, rec_time):
    print('call_back 1:', sub_topic, payload, rec_time)


def cb2(sub_topic, payload, rec_time):
    print('call_back 2:', sub_topic, payload, rec_time)


def cb_stop(sub_topic, payload, rec_time):
    global stop
    print('Received stop request. mqtt_receiver_demo bailing out!')
    stop = True


loc_mqtt.subscribe('#', None)           # All messages ques without callback
# All aap messages willl do this call_back
loc_mqtt.subscribe('aap/#', cb1)
# And if the sub-sub is noot, this one should be called too
loc_mqtt.subscribe('aap/noot/#', cb2)
# And a very special one for the control/stop topic
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
