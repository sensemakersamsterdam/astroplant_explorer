"""
Sample implementation: LCD display.
See https://github.com/sensemakersamsterdam/astroplant_explorer

For the display we do 3 panes. Panes will rotate with a configurable time.
There is one priority pane that will display the specified time and then diasppear.
Panes are the size of the display.
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# Warning: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.


from ae_util.ip import IP_Utils
from ae_drivers.lcd import AE_LCD
from time import sleep, time, strftime, asctime
from ae_util.mqtt import AE_Local_MQTT
from ae_util.configuration import cfg
import json

# global variables
my_cfg = cfg['lcd_display']  # Find our bit in the config file
tick = my_cfg['tick']  # Resolution. Sleep "tick" seconds each loop.


def lcd_setup():
    lcd = AE_LCD('lcd', '16x2 LCD display')
    lcd.setup(erase=True)
    return lcd


def control_cb(sub_topic, payload, rec_time):
    """Handle application control messages.
    """
    global stop_loop
    if payload == 'stop':
        stop_loop = True


def display_cb(sub_topic, payload, rec_time):
    """Handle Display messages.
    """
    try:
        directive = json.load(payload)
    except Exception as ex:
        print('Exception ignored at %s. Probably a bad display directive.\n\rDetails:%s.' %
              (ex, asctime(rec_time))
              )
        return

    print('Got directive', sub_topic, directive)


def expand(txt):
    """Check string for special instruction and replace if found."""
    if txt == '*date_time*':
        return strftime('%d-%m-%Y %H:%M')  # 01-01-2020 18:12
    elif txt == '*time':
        return strftime('%H:%M:%S')  # 01-01-2020 18:12
    elif txt == '*IP*':
        return IP_Utils.get_main_ip_address() or 'no network'
    else:
        return txt


class pane:
    def __init__(self, name, line1, line2, display_time=2, recurring=True):
        self._name = name
        self._disp_time = display_time
        self._recurring = recurring
        self._line0 = line1
        self._line1 = line2
        self._started = None

    def display(self):
        global lcd
        print('Displaying: ', expand(self._line0), expand(self._line1))
        lcd.lcd_string(self._line0, 0)
        lcd.lcd_string(self._line1, 1)
        self._started = time()

    def is_recurring(self):
        """Returns True if pane is repeating"""
        return self._recurring

    def still_on(self):
        """Returns True if pane should still be on"""
        return time() < self._started + self._disp_time if self._started else None

    def reset_time(self):
        self._disp_time = None


class Panes:
    def __init__(self):
        self._queue = []
        self._displaying = None
        self._panes = {}

    def add_or_replace(self, pane, priority=False):
        # TODO add raeplace/update functioality
        # replacement = pane.name in self._panes
        self._panes.append(pane)

    def lcd_tick(self):
        """Called during main loop to find out if something should happen with the LCD."""

        def get_next():
            try:
                self._displaying = next = self._queue.pop(0)
            except IndexError:
                # Nothing to do as it seems
                self._displaying = None
                lcd.lcd_clear()
                return
            next.display()  # Put it on

        active_pane = self._displaying
        if active_pane is None:
            get_next()
        else:
            if active_pane._started - time() > active_pane._disp_time:
                # W're done
                if active_pane._recurring:
                    # Put it back at the end
                    self._queue.append(active_pane)
                get_next()


panes = Panes()
panes.add_or_replace(pane('start',
                          'AstroPlant Xplrr',
                          'Starting up...',
                          display_time=5, recurring=False))
panes.add_or_replace(pane('DT&IP',
                          '*date_time*',
                          '*IP*',
                          display_time=2, recurring=True))
panes.add_or_replace(pane('Sensemakers',
                          '  Sensemakers',
                          'AstroPlant Xplrr',
                          display_time=2, recurring=True))

# Setup the LCD
lcd = lcd_setup()

# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

# Open input channel for application control messages
loc_mqtt.subscribe(cfg['local_MQTT']['control_sub_tpc'], control_cb)

# Open input channel for display messages
loc_mqtt.subscribe(my_cfg['display_sub_tpc'], display_cb)

while not stop_loop:
    panes.lcd_tick()
    sleep(tick)

print('Got stop request. Display exits')
