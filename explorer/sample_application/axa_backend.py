"""
Sample implementation backend interface.
See https://github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.

from ae_util.configuration import cfg
from time import sleep
from ae_util.mqtt import AE_Local_MQTT
import sys

#
# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()
