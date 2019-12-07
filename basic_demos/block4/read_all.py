import datetime  # for timestamp in logfile
import time
import DHT_1x
import waterTemp_1x
import co2_1x
import light_1x
import pathlib  # to test if logfile already exists
import lcdi2c
import subprocess  # to get IP address from shell

try:
    IP = subprocess.check_output(["hostname", "-I"]).decode()
    lcdi2c.display('IP address', str(IP), 10)
except Exception:
    lcdi2c.display('No IP address', '', 10)

lcdi2c.display('Starting', 'measurements', 5)

filename = 'temp_log.csv'
path = pathlib.Path(filename)
if not path.exists():
    # create header row
    csv = open(filename, 'w')
    csv.write("Timestamp, Temperature, Humidity, WaterTemperature, CO2, Light\n")
    csv.close()

while True:
    dt = datetime.datetime.now()
    # for all sensors try to read them, if not make sure the
    # script does not block and fill None in file
    try:
        t = DHT_1x.temperature
        h = DHT_1x.humidity
    except Exception:
        t = None
        h = None
    try:
        wt = waterTemp_1x.read_temp()
    except Exception:
        wt = None
    try:
        co2 = co2_1x.mh_z19()
    except Exception:
        co2 = None
    try:
        l = light_1x.readLight()
    except Exception:
        l = None
    # construct entry to write to file
    entry = str(dt) + ',' + str(t) + ',' + str(h) + ',' + \
        str(wt) + ',' + str(co2) + ',' + str(l) + '\n'
    # print(entry) # for debugging uncomment
    csv = open(filename, 'a')
    try:
        csv.write(entry)
    finally:
        csv.close()
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
