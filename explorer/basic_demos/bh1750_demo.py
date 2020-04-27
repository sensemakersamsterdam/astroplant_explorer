"""
Demo/test program for the AE_BH1750 driver.
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
from ae_drivers.bh1750 import AE_BH1750

bh1750_1 = AE_BH1750('bh1750_1', 'Light')
bh1750_1.setup()

print('BH1750 demo. bh1750_1 prints as:', bh1750_1)
print('and its description is:', bh1750_1.description)

for _ in range(10):
    print('Light=%s lux' % bh1750_1.value())
    sleep(1)
