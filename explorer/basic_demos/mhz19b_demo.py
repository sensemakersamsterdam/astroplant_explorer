"""
Demo/test program for the AE_MHZ19B driver.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

# This program shows some features of the AE_MHZ19B library class

# From the standard time library we only require sleep()
from time import sleep

# And we need the sensor class
from ae_drivers.mhz19b import AE_MHZ19B

# Then we define and initialize the mh-z19b sensor
mhz19b = AE_MHZ19B('mhz19b', 'AE_MHZ19B CO2 sensor')
mhz19b.setup()

print('MH-Z19B CO2 Sensor Demo.')

print('Sensor object prints as %s' % (mhz19b))
print('and its long description is:', mhz19b.description)

print('Now reading values in a loop.\nType Cntl-C to exit this demo.')

try:
    while True:
        print('The current CO2 concentration is %s ppm.' % mhz19b.value())
        sleep(10)

except KeyboardInterrupt:
    print('\nBye bye...')
