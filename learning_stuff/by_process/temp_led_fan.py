# This scripts uses the watertemperature sensor (waterTemp.py) as input. If T <22 a LED will turn on, if T > 22 a Grove Relay with fan will turn on.
import os
import glob
import time
import RPi.GPIO as GPIO
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


try:
    while True:
        # print(read_temp())
        print("Temperatuur: " + str(read_temp()) + " C")
        if read_temp() < 22:
            print("Dit is koud. LED aan en ventilator uit.")
            GPIO.output(20, GPIO.HIGH)
            GPIO.output(16, GPIO.LOW)
        elif read_temp() > 22:
            print("Dit is warm. LED uit en ventilator aan.")
            GPIO.output(20, GPIO.LOW)
            GPIO.output(16, GPIO.HIGH)
        time.sleep(1)
except KeyboardInterrupt:
    print("Gestopt. LED en ventilator uit.")
    GPIO.output(20, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
