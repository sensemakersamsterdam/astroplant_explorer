"""
ae_drivers AE_Relay code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from ._output import _AE_Output


class AE_Relay(_AE_Output):
    """Class to define an on/off Relay. Identical to AE_Output with type_ set to 'Relay'.
    """

    def __init__(self, name, description, *arg, **kwarg):
        super().__init__(name, description, 'Relay', *arg, **kwarg)
