# ToDo: copyright etc
import paho.mqtt.client as mqtt
from configuration import cfg
import json
from time import sleep

ae_id = cfg['ae_id']
base_topic = cfg['local_MQTT']['root_topic'].format(ae_id=ae_id)


class AE_Local_MQTT:
    def __init__(self, clean_session=True):
        self._client = client = mqtt.Client(
            client_id=ae_id, clean_session=True)
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        print('Connect', userdata, flags, rc)
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self._connected = True

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        print('Local MQTT disconnected. Reason: %s Reconnecting' % (str(rc)))
        # ToDo do we need this or is itt automatic...
        self._client.reconnect(clean_session=False)

    def _on_message(self, client, userdata, message):
        print('received', message.topic, message.payload)

    def setup(self):
        self._connected = False
        self._client.connect('localhost')
        self._last_publish = None
        self._subscribed = None
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

    def publish(self, sub_topic, message):
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
        return lp.rc

    def subscribe(self, sub_topic, call_back):
        if self._subscribed is None:
            self._client.subscribe(base_topic + '#')
            print(base_topic + '#')
            self._subscribed = {}
        self._subscribed[str(sub_topic)] = call_back
