"""
Demo/test program for the MQTT utilities.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

##
#  H O W   T O  U S E
#
# Edit configuration.json and pick a nice 'ae_id' for yourself.
#
# Now start a terminal window #1 on your Pi and run:
#       python 1_mqtt_receiver_demo.py
# To monitor MQTT traffic open a second terminal window #2 and run:
#       mosquitto_sub -v -t "#"
# Then open a terminal window #3 and run:
#       python 1_mqtt_sender_demo.py
# This should get things starting. You can run rhe 1_mqtt_sender_demo.py
# repeatedly. The 1_mqtt_receiver_demo and mosquitto_sub will show the
# messages each time you run it.
# And if you want to send the stop-request to the 1_mqtt_receiver_demo.py, run
#       python 1_mqtt_stop_demo.py
# in terminal window #3.
# The mosquitto_sub in terminal #2 you can abort with control-c.

###
# Warning: if import of ae_* module(s) fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae 'lib' directory
# should be included in the printed path

# First we import the variable 'cfg' from the configuration library.
# it reads the JSON file configuration.json from your current directory
# and makes it available to this script as a the dictionary 'cfg'.
from ae_util.configuration import cfg
import sys
sys.path.append('../lib')

# From the standard time library we now import the function sleep()
from time import sleep

# From the mqtt library we import the AE_Local_MQTT class which contains a bunch
# of functions we will use in this script
from ae_util.mqtt import AE_Local_MQTT

# Here we initialize our local MQTT agent.
# It imports your MQTT settings automatically from the configuration.json file.
loc_mqtt = AE_Local_MQTT()

# And now we activate the MQTT connection.
loc_mqtt.setup()

# For the rest it is simple. We send some stuff and print the return code.
# We sleep a bit, send again etc.
# and then we are done.

# Send in sequence a dictionary, a string and an integer.
# A dict will be jsautomatically be JSON formatted before sending.
# All other stuff is formatted to a str first.
print('sub-topic: dict', loc_mqtt.publish('dict', cfg))
sleep(0.4)
print('sub-topic: str', loc_mqtt.publish('string',
                                         'waar eens de boterbloemen bloeiden'))
print('sub-topic: int', loc_mqtt.publish('int', 33))

# sleeeeeeeppppp...
print('Take 5')
sleep(5)

# And send some more
#
print('sub-topic: aap', loc_mqtt.publish('aap', 'payload for aap'))
print('sub-topic: aap/noot', loc_mqtt.publish('aap/noot', 'payload for aap/noot'))
print('sub-topic: test', loc_mqtt.publish('test',
                                          {"topic": "test", "payload": [44, 33]}))

print('And 4 more...')

# Sleep and quit.
sleep(1)

print('Bye bye..')
print('Remember, you can run 1_mqtt_stop_demo.py to stop the 1_mqtt_receiver_demo,')
print('or run this program again.')
