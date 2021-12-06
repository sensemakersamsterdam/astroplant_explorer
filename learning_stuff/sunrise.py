#!/usr/bin/python

import smbus
from time import sleep
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

DEVICE = 0x68  # Default device I2C address

bus = smbus.SMBus(1)  # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
# Rev 1 Pi uses bus 0
REG_CO2_DATA = 0x06
sleep(1)


def readSunrise(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, REG_CO2_DATA, 2)
    co2_true = int.from_bytes(bytes(data), byteorder='big', signed=True)
    print(f' raw data is {data}')
    return co2_true


def main():
    for i in range(0, 11):
        test = b'\x02\xBC'
        print(f'test is {test[0]} and {test[1]}')
        co2 = int.from_bytes(test, byteorder='big', signed=True)
        print(f'reference co2 is {co2}')
        co2_true = readSunrise(DEVICE)
        print(f' true co2 value is {co2_true}')
        sleep(2)


if __name__ == "__main__":
    main()
