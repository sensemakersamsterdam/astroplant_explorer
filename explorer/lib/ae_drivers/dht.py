"""
ae_drivers DHT11 and DHT22(like) code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

from . import _AE_Peripheral_Base
from adafruit_dht import DHT11, DHT22


class AE_DHT(_AE_Peripheral_Base):
    """This class is to define a DHT type temperature/humidity sensor.
    """

    def __init__(self, name, description, pin, sensor=DHT22, retries=4, delay=0.5):
        assert sensor in [DHT11, DHT22], \
            'Supported sensors are DHT11, DHT22. If your sensor is AM2302, you use DHT22'
        assert pin.__class__.__name__ == 'AE_Pin' and pin.value[2] == 'DHT', \
            'Specify parameter "pin" as AE_Pin DHT enum.'
        assert isinstance(retries, int) and 1 <= retries <= 20, \
            'Parameter "retries" is integer between 1 and 20 inclusive.'
        assert isinstance(delay, float) and 0.2 <= delay <= 5.0, \
            'Parameter "delay" is float between 0.2 and 5.0 seconds inclusive.'
        super().__init__(name, description, 'DHT' + str(sensor))
        self._pin = pin
        self._retries = retries
        self._delay = delay
        self._sensor = sensor(pin)

    def _str_details(self):
        return 'pin %s(gpio=%d, conn=%d), values=%s' % (self._pin.name,
                                                        self._pin.value[0],
                                                        self._pin.value[1],
                                                        str(self.values()))

    def values(self):
        """humidity and temperature current readings.
        It makes sure a reading is available

        Raises RuntimeError exception for checksum failure and for insuffcient
        data returned from the device (try again)"""
        return self.humidity(), self.temperature()

    def temperature(self):
        """temperature current reading. It makes sure a reading is available

        Raises RuntimeError exception for checksum failure and for insuffcient
        data returned from the device (try again)"""
        return self._sensor.temperature()

    def humidity(self):
        """humidity current reading. It makes sure a reading is available

        Raises RuntimeError exception for checksum failure and for insuffcient
        data returned from the device (try again)"""
        return self._sensor.humidity()

    def setup(self, **kwarg):
        # Nothing to do
        pass
