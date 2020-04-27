"""
Demo/test program for the DS18B20 driver.
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
from ae_drivers.ds18b20 import AE_DS18B20

ds18b20_1 = AE_DS18B20('ds18b20_1', '(Water)Temperature')
ds18b20_1.setup()

print('DS18B20 demo. ds18b20_1 prints as:', ds18b20_1)
print('and its description is:', ds18b20_1.description)

for _ in range(10):
    print('Water temperature=%s Celsius' % ds18b20_1.value())
    sleep(1)
