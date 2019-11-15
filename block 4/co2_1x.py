# http://eleparts.co.kr/data/design/product_file/SENSOR/gas/MH-Z19_CO2%20Manual%20V2.pdf
# http://qiita.com/UedaTakeyuki/items/c5226960a7328155635f
import serial
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def mh_z19():
  ser = serial.Serial('/dev/ttyS0',
                      baudrate=9600,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=1)
  while 1:
    command = "\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    #result=ser.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
    result=ser.write(bytes(command, 'latin1'))

    s=ser.read(9)
    s = s.decode('latin1')
    #print(s)
    if s[0] == "\xff" and s[1] == "\x86":
      #return {'co2': ord(s[2])*256 + ord(s[3])}
      return ord(s[2])*256+ord(s[3])
   
print(mh_z19())
