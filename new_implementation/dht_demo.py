from ae_explorer import AE_Pin
from ae_explorer.ae_dht import AE_DHT, DHT22
from time import sleep

dht1 = AE_DHT('DHT1', 'Air temperature and humidity', AE_Pin.DHT, sensor=DHT22)
dht1.setup()

print('DHT demo. dht1 prints as:', dht1)
print('and its description is:', dht1.description)

for _ in range(10):
    hum, temp = dht1.values()
    if hum is None or temp is None:
        print('DHT read error!')
    else:
        print('Humidity=%d%%, temperature=%dC' % (hum, temp))
    sleep(1)
