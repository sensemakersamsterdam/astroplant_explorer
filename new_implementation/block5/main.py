from time import sleep
if True:
    import sys
    sys.path.append('..')
    from ae_util.mqtt import AE_Local_MQTT


loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

aap = {'lola': 'een', 'bola': [1, 4, 5], 'one_more': {1: 2, 3: 4}}
print('dict',loc_mqtt.publish('dict', aap))
print('str',loc_mqtt.publish('string', 'waar eens de boterbloemen bloeiden'))
print('int',loc_mqtt.publish('int', 33))

loc_mqtt.subscribe('lola', None)
sleep(20)