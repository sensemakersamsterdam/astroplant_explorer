"""
Demo/test program for the AE_DHT driver.
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
from time import sleep

dht1 = AE_DHT('dht1', 'Air temperature and humidity', AE_Pin.DHT, sensor=DHT22)
dht1.setup()


print('DHT demo. dht1 prints as:', dht1)
print('and its description is:', dht1.description)

for _ in range(10):
    hum, temp = dht1.values()
    if hum is None or temp is None:
        print('DHT read error!')
    else:
        print('Humidity=%d%%, temperature=%dC' % (hum, temp))
    sleep(1)
