"""
Demo/test program for the MQTT utilities.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""

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

# From the mqtt library we import the AE_Local_MQTT class which contains a bunch
# of functions we will use in this script.
from ae_util.mqtt import AE_Local_MQTT

# Here we initialize our local MQTT agent.
# It imports your MQTT settings automatically from the configuration.json file.
loc_mqtt = AE_Local_MQTT()

# And now we activate the MQTT connection.
loc_mqtt.setup()

# And now we just send (publish) the empty stop message. Just sending the
# control/stop topic is sufficiently here.
loc_mqtt.publish('control/stop')
