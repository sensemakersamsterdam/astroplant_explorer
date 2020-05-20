Astroplant Explorer - advanced Python
=====================================
Prerequisites
-------------

The following software needs to be installed on your Raspberry Pi:

1. Raspberry Pi software updated. Use:<br/>`sudo apt update`<br/>and when done<br/>`sudo apt upgrade`
1. I2C, 1Wire and Serial interfaces properly configured. Use the `sudo raspi-config` command for this<br/>In its menu you need: "5 - Interfacing options":
   * For the LCD (and future I2C interfaces) **enable** "P5 - I2C"
   * For the Co2 sensor **enable** "P6 - Serial" but do **not enable** the login shell on the port.
   * For the DS18B20 water temperature **enable** "P7 - 1Wire"

1. For Python 3 & libraries you need:
   * python 3.5.x or higher. Use `python3 -V` to check.
   * pip 19.x.x or higher. Use `pip3 -V` to check.
   * RPi.GPIO library.
   * smbus library.

   To install (or upgrade) this lot use <br/>`sudo apt --upgrade install python3 python3-pip python3-rpi.gpio python3-smbus i2c-tools`<br/>and then check versions again.
   To check your i2c use: `sudo i2cscan -y 1`<br/>This should -with the standard AE kit- show your lcd display and possibly more.

1. Extend your PYTHONPATH. Edit the ".profile" file in your home dir
ectory (no sudo!). Add the lines:<br/>
    `PYTHONPATH=../lib`
    <br/>
    `export PYTHONPATH`
  <br/>to the end of the file. To test this first log out and back in. This causes the .profile to be executed. Then use the command:<br/>
  `python3 -c 'import sys; print(sys.path)'`<br/>
This will print the Python search path. The second one in the list is the one you have just added. It should be like:<br/>'/home/**_your user name_**/**_your ae new directory_**/lib'.

1. Python 3.x will now be accessible with `python3` and pip 19.x with `pip3`.  If you make Python 3.x your standard, and you should since versions 2.x are now officially obsoleted, it is conveinient to have `python` and `pip` to execute the Python 3 and Pip 19 versions respectively.  To do this ececute:<br/>
`sudo rm -f /usr/bin/python; sudo ln -s /usr/bin/python3 /usr/bin/python`
<br/>and:<br/>
`sudo rm -f /usr/bin/pip; sudo ln -s /usr/local/bin/pip3 /usr/bin/pip`

1. The various AstroPlant Explorer programs will communicate to eachother using the MQTT message broker. Hence we will need Mosquitto MQTT broker. This can be done with `sudo apt --upgrade install mosquitto mosquitto-tools`

