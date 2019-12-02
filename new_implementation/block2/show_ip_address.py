"""
Demo/test program for the AE_LCD and the IP utilities drivers.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from ae_drivers.lcd import AE_LCD
from ae_util.ip import IP_Utils

lcd = AE_LCD()
lcd.setup(erase=False)

ip_address = IP_Utils.get_main_ip_address() or 'no IP Address'
print('My main IP address is:', ip_address)
lcd.lcd_string(ip_address, 0)
