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
# And we need the Button driver class
from ae_drivers.mhz19b import AE_MHZ19B

# Then we define and initialize Button 1
co2 = AE_MHZ19B('co2', 'Our hopefully working AE_MHZ19B CO2 sensor')
co2.setup()

print('CO2 demo.')

print('co2 object prints as %s' % (co2))
print('  and its long description is:', co2.description)

print('Now reading values in a loop.\nType Cntl-C to exit this demo.')

try:
    while True:
        print('The currend CO2 concentration is %s ppm.' % co2.value())
        sleep(10)

except KeyboardInterrupt:
    print('\nBye bye...')
