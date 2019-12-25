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
from ae_drivers.button import AE_Toggle_Button
from time import sleep

# Setup button 1
tgl1 = AE_Toggle_Button('tgl1', 'Just toggle button 1', AE_Pin.D5)
tgl1.setup()
last_tgl_state = 0
#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

print('\nType Cntl-C to exit and press button 1...')
print('button over MQTT demo.')
print('values published under topic: button1' )

try:
    while True:
        if tgl1.state() != last_tgl_state:
            print('sub-topic: button', loc_mqtt.publish('button1', tgl1.state()))
            last_tgl_state = tgl1.state()
            sleep(0.1) #delay a bit
except KeyboardInterrupt:
    print('\nBye bye...')

