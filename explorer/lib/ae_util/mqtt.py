"""
ae_util mctt module code.
See https: // github.com/sensemakersamsterdam/astroplant_explorer
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#

import paho.mqtt.client as mqtt
from ae_util.configuration import cfg
import json
import os
from time import sleep, time

ae_id = cfg['ae_id']
base_topic = cfg['local_MQTT']['root_topic'].format(ae_id=ae_id)


class AE_Local_MQTT:
    def __init__(self, clean_session=True, client_id=None):
        self._client_id = ae_id + \
            str(os.getpid()) if client_id is None else client_id
        self._client = client = mqtt.Client(
            client_id=self._client_id, clean_session=True)
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        # print('Connect', userdata, flags, rc)
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self._connected = True

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        print('Local MQTT disconnected. Reason: %s Reconnecting' % (str(rc)))
        # ToDo do we need to do the reconnect or is it automatic...
        # self._client.reconnect(clean_session=False)

    def setup(self):
        self._connected = False
        self._last_publish = None
        self._in_queue = []
        self._client.connect('localhost')
        self._client.loop_start()

    def __clr__(self):
        if self._last_publish is not None:
            try:
                self._last_publish.wait_for_publish()
            except Exception as ex:
                print(ex)
                pass
        self._client.disconnect()
        self._client.loop_stop()

    def publish(self, sub_topic, message=None):
        if isinstance(message, dict):
            msg = json.dumps(message)  # format as json
        else:
            msg = str(message)
        for _ in range(40):
            if not self._connected:
                sleep(0.05)
            else:
                break
        else:
            return None
        self._last_publish = lp = self._client.publish(
            base_topic + sub_topic, msg)
        sleep(0.1)  # To avoid race condition in loop-thread
        return lp.rc

    def _rcve_message(self, client, userdata, message, call_back):
        received_time = time()
        topic = message.topic
        payload = message.payload.decode()
        # ToDo message also contains qos and retain flags. Should we pass them on too?
        sub_topic = topic.replace(base_topic, '', 1)
        # print('received', message.topic, sub_topic, message.payload, call_back)
        if call_back is not None:
            # print('calling', call_back)
            call_back(sub_topic, payload, received_time)
        else:
            #print('queueing')
            self._in_queue.append((sub_topic, payload, received_time))

    def subscribe(self, sub_topic, call_back=None):
        topic = base_topic + sub_topic
        self._client.message_callback_add(topic,
                                          lambda client, userdata, message:
                                          self._rcve_message(client, userdata, message, call_back))
        self._client.subscribe(topic)

    def unsubscribe(self, sub_topic):
        topic = base_topic + sub_topic
        self._client.unsubscribe(topic)
        self._client.message_callback_remove(topic)

    def get_message(self):
        try:
            return self._in_queue.pop(0)
        except IndexError:
            # Queue was empty
            return None, None, time()
