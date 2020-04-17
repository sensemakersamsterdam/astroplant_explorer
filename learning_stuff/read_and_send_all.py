# Import all the necessary libraries
from time import sleep, time
import datetime  # for timestamp in datalogfile
import pathlib  # to test if datalogfile already exists
import DHT22 #if you have a DHT22 sensor otherwise outcomment
#import bme280 #if you have a BME280 sensor instead of an DHT22
import waterTemp
import co2
import bh1750
import lcdi2c
import paho.mqtt.client as mqtt  # paho.mqtt is the mqtt protocol
# credentials is a module made by sensemakers with the credentials to the SURF cloud platform
import credentials
import json
import logging #to create error and debug logfile

# Define logger details
astro_logger = logging.getLogger('AstroplantExplorer')
astro_logger.setLevel(logging.DEBUG)   # or logging.INFO after the debugging phase
# create file handler which logs even debug messages
fh = logging.FileHandler('astroplant_explorer.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
astro_logger.addHandler(fh) 
astro_logger.addHandler(ch)
# Define the MQTT settings
mqtt_client = mqtt.Client()
mqtt_server_ip = credentials.my_mqtt_host
# using credentials module
mqtt_client.username_pw_set(
    credentials.my_mqtt_user, credentials.my_mqtt_password)
mqtt_client.connect(mqtt_server_ip, port=9998, keepalive=120)  # using credentials module
mqtt_client.loop_start()
# topic is necessary for the SURF platform / we should move this to credentials
topic = 'pipeline/astroplant/AstroPlantExplorer.YourNameHere'
mqtt_client.enable_logger(logger=astro_logger)

# initiate measurements
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
    for _ in range(2):
        try:
            msg = '{"app_id":"astroplant", "dev_id":"AstroPlantExplorer.YourNameHere", "payload_fields": %s}' % json.dumps(params)
            result = mqtt_client.publish(topic, msg)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                return
            elif result.rc == mqtt. MQTT_ERR_NO_CONN:
                astro_logger.info('reconnecting MQTT')
                mqtt_client.reconnect()
            else:
                astro_logger.error("Cannot publish, rc=%d, topic=%s, msg=%s", result.rc. topic, msg)
                return
        except Exception as ex:
            astro_logger.exception(ex)     # Log exception info and continue…
            return

csv_fields = ["meas_time", "temp", "hum", "watertemp", "CO2", "light"]

measurement_interval = 60
while True:
    t_start = datetime.datetime.now()
    params = {}

    # for all sensors try to read them, if not make sure the script
    # does not block and fill None in file
    params["meas_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        h, t = DHT22.readSensor()
        #t, p, h = bme280.readBME280All() #use this for bme280 and outcomment line above
        params["hum"] = h
        params["temp"] = t
    except Exception as ex:
        astro_logger.exception(ex)     # Log exception info and continue…
        pass

    try:
        wt = waterTemp.read_temp()
        params["watertemp"] = wt
    except Exception as ex:
        astro_logger.exception(ex)     # Log exception info and continue…
        pass

    try:
        CO2 = co2.mh_z19()
        params["CO2"] = CO2
    except Exception as ex:
        astro_logger.exception(ex)     # Log exception info and continue…
        pass

    try:
        light = bh1750.readLight()
        params["light"] = light
    except Exception as ex:
        astro_logger.exception(ex)     # Log exception info and continue…
        pass

    entry = ""
    for field in csv_fields:
        entry += str(params.get(field, "")) + ","
    entry = entry[:-1] + "\n"   # Replace last comma by newline

    with open(filename, 'a') as csv:
        csv.write(entry)
    #    print(entry)

    # call the MQTT function with the parameters to send this data to SURF cloud platform
    SMA_send(params)
    print(params)

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
        lcdi2c.display('co2', str(round(CO2, 2)) + ' ppm', 5)
    else:
        lcdi2c.display('could not read', 'co2', 5)
    if light is not None:
        lcdi2c.display('light', str(round(light, 2)) + ' lux', 5)
    else:
        lcdi2c.display('could not read', 'light', 5)
    timedelta = (datetime.datetime.now()- t_start)
    time_left = measurement_interval - (timedelta.days * 24 * 3600 + timedelta.seconds)
    if time_left < 1:
        time_left = 1
    for i in range(time_left, 0, -1):
        lcdi2c.display(' ', str(i), 1)
