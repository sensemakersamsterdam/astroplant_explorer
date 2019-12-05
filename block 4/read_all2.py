#Import all the necessary libraries
import datetime # for timestamp in logfile
from time import sleep, time
import DHT_1x
import waterTemp_1x
import co2_1x
import light_1x
import pathlib # to test if logfile already exists
import lcdi2c
import paho.mqtt.client as mqtt #paho.mqtt is the mqtt protocol
from credentials import * #credentials is a module made by sensemakers with the credentials to the SURF cloud platform
import json

#Define the MQTT settings
sensor_id = "AstroPlantExplorer.user" #change "user" to your own name
mqtt_client = mqtt.Client()
mqtt_server_ip = my_mqtt_host
mqtt_client.username_pw_set(my_mqtt_user, my_mqtt_password) #using credentials module 
mqtt_client.connect(mqtt_server_ip, port=9998) #using credentials module
topic = 'pipeline/WON/' + sensor_id #topic is necessary for the SURF platform / we should move this to credentials

#initiate the lcd
lcdi2c.display('Starting','measurements',5)#display this text for 5 sec

#create a csv log file
filename = 'sensor_log.csv'
path = pathlib.Path(filename)
if not path.exists():
  #create header row
  csv = open(filename, 'w')
  csv.write("Timestamp, Temperature, Humidity, WaterTemperature, CO2, Light\n")
  csv.close()

#create the json string for MQTT
def SMA_send(**params):
        mqtt_client.publish(topic, '{"app_id":"WON", "dev_id": "' + \
        sensor_id + '", "payload_fields": %s}' % json.dumps(params))

while True:
  dt = datetime.datetime.now()
  # for all sensors try to read them, if not make sure the script does not block and fill None in file
  try:
    h,t = DHT_1x.readSensor()
  except:
    th,  = None
  try:
    wt = waterTemp_1x.read_temp()
  except:
    wt = None
  try:
    co2 = co2_1x.mh_z19()
  except:
    co2 = None 
  try:
    l = light_1x.readLight()
  except:
    l = None
  #construct entry to write to file
  entry = str(dt) + ',' + str(t) + ',' + str(h) + ',' + str(wt) + ',' + "0" + "," + str(l) + '\n' #+ str(co2) + ','
  # print(entry) # for debugging uncomment
  csv = open(filename, 'a')
  try:
    csv.write(entry)
    print(entry)
  finally:
    csv.close()
  # send the MQTT string with this data to SenseMakers Amsterdam backend
  try:
      SMA_send(temp=t, hum=h)
  except Exception:
    print('problem sending')
    SMA_send(fail=1)

 
 # show measurements on display for 5 seconds each
  if t is not None:
    lcdi2c.display('air temperature',str(round(t, 2)) + ' C',5)
  else:
    lcdi2c.display('could not read','air temperature',5)
  if h is not None:
    lcdi2c.display('rel. humidity',str(round(h, 2)) + ' %',5)
  else:
    lcdi2c.display('could not read','humidity',5)
  if wt is not None:
    lcdi2c.display('water temp',str(round(wt, 2)) + ' C',5)
  else:
    lcdi2c.display('could not read','water temp',5)
  if co2 is not None:
    lcdi2c.display('co2',str(round(co2, 2)) + ' ppm',5)
  else:
    lcdi2c.display('could not read','co2',5)
  if l is not None:
    lcdi2c.display('light',str(round(l, 2)) + ' lux',5)
  else:
    lcdi2c.display('could not read','light',5)
  for i in range(35, 0, -1):
    lcdi2c.display(' ',str(i),1)

