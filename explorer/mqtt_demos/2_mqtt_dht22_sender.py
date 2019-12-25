"""
Demo/test program to send DHT measurements over MQTT.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from time import sleep
from ae_drivers import AE_Pin
from ae_drivers.dht import AE_DHT, DHT22
from ae_util.configuration import cfg
from ae_util.mqtt import AE_Local_MQTT

# Setup DHT sensor
dht1 = AE_DHT('dht1', 'Air temperature and humidity', AE_Pin.DHT, sensor=DHT22)
dht1.setup()

# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

print('\nType Cntl-C to exit and press button 1...')
print('DHT over MQTT demo.')
print('values published under topic: dht22' )

try:
    while True:
        hum, temp = dht1.values()
        if hum is None or temp is None:
            print('DHT read error!')
        else:
            print('dht22', loc_mqtt.publish('dht22', 'Humidity=%d%%, temperature=%dC' % (hum, temp)))
        sleep(3)

except KeyboardInterrupt:
    print('\nBye bye...')
