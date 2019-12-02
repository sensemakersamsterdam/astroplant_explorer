"""
ae_drivers DS18B20 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral_Base


class AE_DS18B20(_AE_Peripheral_Base):
    """Class to control a DS18B20 temperature sensor
    """

    def __init__(self, *arg, **kwarg):
        raise NotImplementedError
