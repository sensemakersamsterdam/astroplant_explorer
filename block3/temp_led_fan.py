"""This scripts uses the watertemperature sensor (waterTemp.py) as input.
If T <22 a LED will turn on, if T > 22 a Grove Relay with fan will turn on.
Uses the w1-therm module. Will return the temp of the first sensor found if
multiple DS18B20 modules are on the same 1-wire bus.
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function
import os
import glob
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
# Select first one of the DS18B20's on the bus.
device_folder = glob.glob(base_dir + '28*')[0]
if not device_folder:
    print("Geen temperatuursensor op GPIO 4 gevonden.")
    sys.exit(1)

device_file = device_folder + '/w1_slave'


def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()


def read_temp():
    lines = read_temp_raw()
    while not lines[0].strip().endswith('YES'):
        # Keep trying every 0.2 sec until first ends with YES.
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        return float(temp_string) / 1000.0
    else:
        raise EOFError('No temperature found')


print('Type cntl-c om dit programma te stoppen...')
try:
    while True:
        # print(read_temp())
        print("Temperatuur: " + str(read_temp()) + " C")
        if read_temp() < 22:
            print("Dit is koud. LED aan en ventilator uit.")
            GPIO.output(AE.LED1, GPIO.HIGH)
            GPIO.output(AE.RY1, GPIO.LOW)
        elif read_temp() >= 22:
            print("Dit is warm. LED uit en ventilator aan.")
            GPIO.output(AE.LED1, GPIO.LOW)
            GPIO.output(AE.RY1, GPIO.HIGH)
        sleep(15)
except KeyboardInterrupt:
    print("Gestopt. LED en ventilator uit.")
    GPIO.output(AE.RY1, GPIO.LOW)
    GPIO.output(AE.LED1, GPIO.LOW)
    GPIO.cleanup()
