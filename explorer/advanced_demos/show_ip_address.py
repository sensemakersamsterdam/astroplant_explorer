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

# This demo will show your IP address on the display and the console.
# If you have more than one IP Address it will show the one with the
# cheapest route. And if networking is off it will show 'no IP Address'

# Get qnd initialize the LCD library
from ae_drivers.lcd import AE_LCD
# and the IP utilities library
from ae_util.ip import IP_Utils

# Define the display
lcd = AE_LCD('lcd', '16x2 LCD display')
# And initialize it without erasing.
lcd.setup(erase=False)

# Now get our main IP addres. If none found use the "no IP" text.
# Read about "Python short circuit evaluation" if you want to understand.
ip_address = IP_Utils.get_main_ip_address() or 'no IP Address'

# Finally print and display the results.
print('My main IP address is:', ip_address)
lcd.lcd_string(ip_address, 0)
