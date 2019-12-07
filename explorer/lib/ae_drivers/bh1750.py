"""
ae_drivers BH1750 code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral_Base


class AE_BH1750(_AE_Peripheral_Base):
    """Class to control a BH 1750 light intensity sensor
    """

    def __init__(self, *arg, **kwarg):
        raise NotImplementedError
