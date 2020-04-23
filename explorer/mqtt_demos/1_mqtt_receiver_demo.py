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

# From the standard time library we now import the function sleep()
from time import sleep
import sys
sys.path.append('../lib')

# From the mqtt library we import the AE_Local_MQTT class which contains a bunch
# of functions we will use in this script
from ae_util.mqtt import AE_Local_MQTT


# Here we initialize our local MQTT agent.
# It imports your MQTT settings automatically from the configuration.json file.
loc_mqtt = AE_Local_MQTT()

# And now we activate the MQTT connection.
loc_mqtt.setup()


# Further down this program loops, doing the same code over and over again, until
# we set the following global variable to 'True'
stop = False

# Now we define a so-called call-back function. This fuction is automatically
# executed when 'something' happens.  What 'something' is in this case comes
# further down. Here we just define that we do a print when 'something' happens.


def cb1(sub_topic, payload, rec_time):
    print('call_back 1:', sub_topic, payload, rec_time)

# And here we have more of the same. It will be executed when 'another something'
# happens. And the print out is also a wee bit different.


def cb2(sub_topic, payload, rec_time):
    print('call_back 2:', sub_topic, payload, rec_time)

# And here in number three. It will be called when 'something #3' happens.
# But it is different than the ones before. It actually does something.
# It sets the variable 'stop' to 'True'. Look again at the explanation
# a couple of lines higher when we initialized the 'stop' variable.
# what do you think that will happen when this function runs?


def cb_stop(sub_topic, payload, rec_time):
    global stop
    print('Received stop request. 1_mqtt_receiver_demo bailing out!')
    stop = True


# In this script we want to recaive MQTT messages. So we need to tell MQTT what
# we want it to send to us. We do this by subscribing to so called 'topics'
# The topic '#' is special. It just means everything. Aren't we greedy?
# We also tell MQTT to stash the incoming messages for us for later pick-up.
loc_mqtt.subscribe('#', None)           # All messages ques without callback

# ANd here we will do another subscription. This time the topic needs to start
# with 'aap/'. Remember that '#' means anything, so we subscribe to 'aap/one'
# and 'aap/two' and indefinately more.
# and this time we also tell mqtt to run the function 'cb1' when we actually
# get a message with a topic that starts with 'aap/'.
# So (please read the coment back where cb1() was defined), the 'something'
# for 'cb1()' is nothing other than recieving a message with a topic that starts
# with 'aap/'.
loc_mqtt.subscribe('aap/#', cb1)

# And the 'another something' we need to happen for 'cb2()' to run is nothing more
# than receiving a message with a topic starting with 'aap/noot/'.
# But hey, 'aap/noot' also starts with 'aap/'. And this is will trigger the 'cb1()'
# call back too. So if I send 'aap/noot/yes', then both cb1() and cb2() will be
# run.  But if I send 'aap/hello', then only cb1() will run.
loc_mqtt.subscribe('aap/noot/#', cb2)

# And now the 3rd one for the 'control/stop' topic. When we get exactly this one,
# we will run the 'cb_stop()' call-back. Which will .....
loc_mqtt.subscribe('control/stop', cb_stop)

# Finally our main loop. Which will run until 'stop' will be set to
# true, or alternatively when we do a manual abort with contol-c
print('Abort with control-c to end prematurely.')
try:
    while not stop:
        # Remember that we also did a subscription to '#', meaning
        # everything. And without a call-back. Which means that MQTT
        # will stash incoming messages for later pick-up?
        # Well, in the line below we check and get the oldest
        # message in the stash, and -if found- print its content.
        sub_topic, payload, rec_time = loc_mqtt.get_message()
        if sub_topic is not None:
            print('Dequeued:', sub_topic, payload, rec_time)
        sleep(0.1)
except KeyboardInterrupt:
    print('\nManually aborted....\nBye bye')
