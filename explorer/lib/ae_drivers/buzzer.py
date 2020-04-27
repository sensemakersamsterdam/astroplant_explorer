"""
ae_drivers AE_Buzzer code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Ted van der Togt
# Adapted code AE_Relay from Gijs Mos
#

from ._output import _AE_Output


class AE_Buzzer(_AE_Output):
    """Class to define an on/off Buzzer. Identical to AE_Output with type_ set to 'Buzzer'.
    """

    def __init__(self, name, description, *arg, **kwarg):
        super().__init__(name, description, 'Buzzer', *arg, **kwarg)
