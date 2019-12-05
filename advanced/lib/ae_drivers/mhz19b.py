"""
ae_drivers MH-Z19B CO2 sensor code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral_Base


class AE_MHZ19B(_AE_Peripheral_Base):
    """Class to control a MH-Z19B CO2 sensor
    """

    def __init__(self, *arg, **kwarg):
        raise NotImplementedError
