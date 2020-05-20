"""
Sample implementation: MQTT test generator for axa_display.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from time import sleep, time
from ae_util.mqtt import AE_Local_MQTT
from ae_util.configuration import cfg
from os import system

# global variables
my_cfg = cfg['lcd_display']  # Find our bit in the config file

loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

print('** test_axa_display: sending stop request to other axa programs...')
# Stop other stuff during test.
loc_mqtt.publish(cfg['local_MQTT']['control_sub_tpc'], 'stop')
print('** test_axa_display: starting fresh axa_display...')
system('python axa_display.py&')
sleep(5)

test_cases = [
    (-1, '1- one time message, 10 secs, no priority.',
        (
            '{"action":"upsert", "id":"p1", "l1":"line - 1", "l2":"test 1", "secs":5}',
        )
     ),
    (-1, '2- recurring message, 1 secs.',
        (
            '{"action":"upsert", "id":"p2", "l1":"line - 1", "l2":"test 2", "secs":1, "recur":true}',
        )
     ),
    (-1, '3- update recurring message, 2 secs.',
        (
            '{"action":"upsert", "id":"p2", "l1":"line - 1 - upd!", "l2":"test 3", "secs":2, "recur":true}',
        )
     ),
    (-1, 'End of the tests...',
         (
             '{"action":"delete", "id":"p2"}',
             '{"action":"delete", "id":"info"}',
             '{"action":"delete", "id":"logo"}',
             '{"action":"upsert", "id":"end1", "l1":"This is the end", "l2":" ", "recur":true, "secs":1}',
             '{"action":"upsert", "id":"end2", "l2":"Bye, bye...", "recur":true, "secs":0.5}',
         ),
     ),
]

for test_case in test_cases:
    wait_time, msg, directives = test_case
    if wait_time >= 0:
        print('** test_axa_display: sleeping %d seconds...' % wait_time)
        sleep(wait_time)
    else:
        input('** test_axa_display: type return to contine.............')

    print('\n\r** test_axa_display: next test: %s...' % msg)
    for directive in directives:
        loc_mqtt.publish(my_cfg['display_sub_tpc'], directive)

print('** test_axa_display: sleeping 10 seconds...')
sleep(10)
print('** test_axa_display: sending stop request to other axa programs...')
loc_mqtt.publish(cfg['local_MQTT']['control_sub_tpc'], 'stop')
