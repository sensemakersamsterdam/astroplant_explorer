# ToDO copyright etc.
if True:
    import sys
    sys.path.append('..')
    from ae_drivers.lcd import AE_LCD
    from ae_util.ip_utils import IP_Utils

lcd = AE_LCD()
lcd.setup(erase=False)

ip_address = IP_Utils.get_main_ip_address() or 'no IP Address'
print('My main IP address is:', ip_address)
lcd.lcd_string(ip_address, 0)
