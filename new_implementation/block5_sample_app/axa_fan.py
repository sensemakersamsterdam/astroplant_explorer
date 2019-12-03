"""
Sample implementation: Case fan control.
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
import json

# global variables
my_cfg = cfg['fan_control']     # Find out bit in the config file
stop_loop = False
publish_sub = my_cfg['publish_sub']
sensor_name = my_cfg['name']
threshold_temp = my_cfg['threshold_temperature']

dht_sub_topic = cfg['dht_air']['publish_sub']
dht_sensor_name = cfg['dht_air']['name']

temperature = None
humdity = None


def setup_fan():
    from ae_drivers import AE_Pin, OFF
    from ae_drivers.relay import AE_Relay
    # Pull the parameters from the config file and 'cast' to proper type
    pin = eval('AE_Pin.' + my_cfg['AE_Pin'])
    desc = my_cfg['description']
    # Create sensor object and get it going
    fan = AE_Relay(sensor_name, desc, pin, initial_state=OFF)
    fan.setup()
    return fan


def control_cb(sub_topic, payload, rec_time):
    """Handle application control messages.
    """
    global stop_loop
    if payload == 'stop':
        stop_loop = True
        fan.off()


def dht_cb(sub_topic, payload, rec_time):
    """Handle DHT messages.
    """
    global temperature, humidity
    try:
        result = json.loads(payload)
        if result[dht_sensor_name]['samples'] > 0:
            temperature = result[dht_sensor_name]['temperature']
            humidity = result[dht_sensor_name]['humidity']
    except Exception as ex:
        print('Fan', ex)


# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

# Setup fan in off state
fan = setup_fan()

# Open input channel for application control messages
loc_mqtt.subscribe('control', control_cb)


# open input channel for sensor messages
loc_mqtt.subscribe(dht_sub_topic, dht_cb)

while not stop_loop:
    # print(temperature)
    if temperature is not None:
        if temperature >= threshold_temp and fan.is_off():
            fan.on()
            state = 'to_on'
        elif temperature < threshold_temp and fan.is_on():
            fan.off()
            state = 'to_off'
        elif fan.is_off():
            state = 'is_off'
        else:
            state = 'is_on'

        loc_mqtt.publish(publish_sub, {
            sensor_name: {
                'time': int(time()),
                'fan_state': state
            }
        })

    sleep(5)

fan.off()
print('Got stop request. Fan control Exits')
