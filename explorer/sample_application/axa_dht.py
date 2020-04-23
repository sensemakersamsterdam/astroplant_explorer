"""
Sample implementation: DHT sensor poller/averager/publisher.
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

# global variables
my_cfg = cfg['dht_air']     # Find out bit in the config file
stop_loop = False
publish_interval = my_cfg['pub_interval']
measurement_interval = my_cfg['meas_interval']
publish_sub = my_cfg['publish_sub']
sensor_name = my_cfg['name']


def setup_dht():
    from ae_drivers import AE_Pin
    from ae_drivers.dht import AE_DHT, DHT11, DHT22
    # Pull the parameters from the config file and 'cast' to proper type
    pin = eval('AE_Pin.' + my_cfg['AE_Pin'])
    sensor = eval(my_cfg['dht_type'])

    desc = my_cfg['description']
    # Create sensor object and get it going
    dht = AE_DHT(sensor_name, desc, pin, sensor=sensor)
    dht.setup()
    return dht


def control_cb(sub_topic, payload, rec_time):
    """Handle application control messages.
    """
    global stop_loop
    if payload == 'stop':
        stop_loop = True


# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

# Open input channel for application control messages
loc_mqtt.subscribe('control', control_cb)

# Set-up sensor.
dht = setup_dht()

sigma_hum = 0
sigma_temp = 0
samples = 0
next_measurement = time() + measurement_interval
next_publish = time() + publish_interval

while not stop_loop:

    if time() >= next_measurement:
        # Do next measurement
        next_measurement += measurement_interval
        hum, temp = dht.values()
        if hum is not None:
            # Got a valid measurement.
            sigma_hum += hum
            sigma_temp += temp
            samples += 1

    if time() >= next_publish:
        # Average results, publish
        data = {sensor_name: {'humidity': round(sigma_hum / samples, 1),
                              'temperature': round(sigma_temp / samples, 1),
                              'samples': samples,
                              'time': int(time())
                              }
                }
        loc_mqtt.publish(publish_sub, data)
        # start new averaging cycle
        sigma_hum = 0
        sigma_temp = 0
        samples = 0
        next_publish += publish_interval
        # print(data)

    sleep(1)

print('Got stop request. DHT Exits')
