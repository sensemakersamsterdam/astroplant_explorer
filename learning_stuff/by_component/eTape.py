# Waterlevel measurement with Milone eTape and Grove 12 bits ADC
# This code is tested with Grove - I2C ADC based on ADC121C021
# Code based on github.com/ControlEverythingCommunity/ADC121C021

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# ADC121C021 address, 0x50(80)
# Select configuration register, 0x02(02)
# Automatic conversion mode enabled, 0x20(32)    
bus.write_byte_data(0x50, 0x02, 0x20)

time.sleep(0.5)

def readLevel():
    # ADC121C021 address, 0x50(80)
    # Read data back from 0x00(00), 2 bytes
    # raw_adc MSB, raw_adc LSB
    data = bus.read_i2c_block_data(0x50, 0x00, 2)
    # Convert the data to 12-bits
    raw_adc = (data[0] & 0x0F) * 256 + data[1]
    # Subtract 0 value and divide by delta raw_adc per millimeter
    waterlevel = (raw_adc - 1064.0) / 2.825
    return (waterlevel)

def main():
    while True:
      # Output data to screen
      print ("Water level : " + str(readLevel()) + " mm.")
      time.sleep(1)
   
if __name__=="__main__":
   main()