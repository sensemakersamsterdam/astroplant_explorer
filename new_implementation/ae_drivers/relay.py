# ToDo: copyright etc.
from ._output import _AE_Output


class AE_Relay(_AE_Output):
    """Class to define an on/off Relay. Identical to AE_Output with type_ set to 'Relay'.
    """

    def __init__(self, name, description, *arg, **kwarg):
        super().__init__(name, description, 'Relay', *arg, **kwarg)
