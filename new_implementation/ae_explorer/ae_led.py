from ._ae_output import _AE_Output


class AE_LED(_AE_Output):
    """Class to define an on/off LED. Identical to AE_Output with type_ set to 'LED'.
    """

    def __init__(self, name, description, *arg, **kwarg):
        super().__init__(name, description, 'LED', *arg, **kwarg)
