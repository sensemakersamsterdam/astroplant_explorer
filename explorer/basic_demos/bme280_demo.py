"""
Demo/test program for the AE_BME280 driver.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Ted van der Togt
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from time import sleep
from ae_drivers.bme280 import AE_BME280

bme280_1 = AE_BME280('bme280_1', 'Air temperature, pressure and humidity')
bme280_1.setup()

print('BME280 demo. bme280_1 prints as:', bme280_1)
print('   and its description is:', bme280_1.description)
print('\r\nReading values 10 times:')

for _ in range(10):
    print('Temperature=%s C, pressure=%s hPa, humidity=%s %%rel,' %
          bme280_1.values())
    sleep(1)
