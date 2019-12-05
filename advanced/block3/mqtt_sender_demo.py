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

#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

#
# Send in sequence a dictionary, a string and an integer. Print the return code.
# A dict will be json formatted before sending. All other stuff is formatted to a string first.
print('sub-topic: dict', loc_mqtt.publish('dict', cfg))
sleep(0.4)
print('sub-topic: str', loc_mqtt.publish('string',
                                         'waar eens de boterbloemen bloeiden'))
print('sub-topic: int', loc_mqtt.publish('int', 33))

print('Take 5')
sleep(5)

#
# And some more
#
print('sub-topic: aap', loc_mqtt.publish('aap', 'payload for aap'))
print('sub-topic: aap/noot', loc_mqtt.publish('aap/noot', 'payload for aap/noot'))
print('sub-topic: test', loc_mqtt.publish('test',
                                          {"topic": "test", "payload": [44, 33]}))

print('And 4 more...')
sleep(4)

print('And now we send a stop message to the receiver and stop ourselves too.')
loc_mqtt.publish('control/stop')
print('Bye bye..')
