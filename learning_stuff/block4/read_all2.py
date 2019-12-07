# Import all the necessary libraries
import datetime  # for timestamp in logfile
from time import sleep, time
import DHT_1x
import waterTemp_1x
import co2_1x
import light_1x
import pathlib  # to test if logfile already exists
import lcdi2c
import paho.mqtt.client as mqtt  # paho.mqtt is the mqtt protocol
# credentials is a module made by sensemakers with the credentials to the SURF cloud platform
import credentials
import json

# Define the MQTT settings
sensor_id = "AstroPlantExplorer.user"  # change "user" to your own name
mqtt_client = mqtt.Client()
mqtt_server_ip = credentials.my_mqtt_host
# using credentials module
mqtt_client.username_pw_set(
    credentials.my_mqtt_user, credentials.my_mqtt_password)
mqtt_client.connect(mqtt_server_ip, port=9998)  # using credentials module
# topic is necessary for the SURF platform / we should move this to credentials
topic = 'pipeline/WON/' + sensor_id

# initiate the lcd
lcdi2c.display('Starting', 'measurements', 5)  # display this text for 5 sec

# create a csv log file
filename = 'sensor_log.csv'
path = pathlib.Path(filename)
if not path.exists():
    # create header row
    csv = open(filename, 'w')
    csv.write("Timestamp, Temperature, Humidity, WaterTemperature, CO2, Light\n")
    csv.close()

# define a function with the json string.


def SMA_send(params):
    try:
        mqtt_client.publish(topic, '{"app_id":"WON", "dev_id": "' +
                            sensor_id + '", "payload_fields": %s}' % json.dumps(params))
    except Exception:
        print('Problem sending to backend via MQTT')


csv_fields = ["meas_time", "temp", "hum", "watertemp", "CO2", "light"]

while True:

    params = {}

    # for all sensors try to read them, if not make sure the script
    # does not block and fill None in file
    params["meas_time"] = datetime.datetime.now()

    try:
        params["hum"], params["temp"] = DHT_1x.readSensor()
    except Exception:
        pass

    try:
        wt = waterTemp_1x.read_temp()
        params["watertemp"] = wt
    except Exception:
        pass

    try:
        co2 = co2_1x.mh_z19()
        params["CO2"] = co2
    except Exception:
        pass

    try:
        light = light_1x.readLight()
        params["light"] = light
    except Exception:
        pass

    entry = ""
    for field in csv_fields:
        entry += params.get(field, "") + ","
    entry = entry[:-1] + "\n"   # Replace last comma by newline

    with open(filename, 'a') as csv:
        csv.write(entry)
        print(entry)

    # call the MQTT function with the parameters to send this data to SURF cloud platform
    SMA_send(params)

    # show measurements on display for 5 seconds each
    if t is not None:
        lcdi2c.display('air temperature', str(round(t, 2)) + ' C', 5)
    else:
        lcdi2c.display('could not read', 'air temperature', 5)
    if h is not None:
        lcdi2c.display('rel. humidity', str(round(h, 2)) + ' %', 5)
    else:
        lcdi2c.display('could not read', 'humidity', 5)
    if wt is not None:
        lcdi2c.display('water temp', str(round(wt, 2)) + ' C', 5)
    else:
        lcdi2c.display('could not read', 'water temp', 5)
    if co2 is not None:
        lcdi2c.display('co2', str(round(co2, 2)) + ' ppm', 5)
    else:
        lcdi2c.display('could not read', 'co2', 5)
    if l is not None:
        lcdi2c.display('light', str(round(l, 2)) + ' lux', 5)
    else:
        lcdi2c.display('could not read', 'light', 5)
    for i in range(35, 0, -1):
        lcdi2c.display(' ', str(i), 1)
