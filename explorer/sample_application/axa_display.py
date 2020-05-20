"""
Sample implementation: LCD display.
See https://github.com/sensemakersamsterdam/astroplant_explorer

Panes are the size of the display.
"""
#
# (c) Sensemakersams.org and others. See https://github.com/sensemakersamsterdam/astroplant_explorer
# Author: Gijs Mos
#
# WARNING: if import of ae_* modules fails, then you need to set up PYTHONPATH.
# To test start python, import sys and type sys.path. The ae module directory
# should be included.


from ae_util.ip import IP_Utils
from ae_drivers.lcd import AE_LCD
from time import sleep, time, strftime, asctime, localtime
from ae_util.mqtt import AE_Local_MQTT
from ae_util.configuration import cfg
import json

# global variables
my_cfg = cfg['lcd_display']  # Find our bit in the config file
tick = my_cfg['tick']  # Resolution. Sleep "tick" seconds each loop.
stop_loop = False


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
    """Handle display messages.
    """
    try:
        directive = json.loads(payload)
        print('Got directive', sub_topic, directive)
        panes.execute(directive)
    except Exception as ex:
        print('Bad directive received at %s.\n\rDetails: %s' %
              (asctime(localtime(rec_time)), ex))
        return


def debug_cb(sub_topic, payload, rec_time):
    print('\n\rDebug (%s) at %s:' % (payload, asctime()))
    print('==Panes==')
    for pane in panes._panes.values():
        print(pane)
    print('==Queue==')
    for pane in panes._queue:
        print(pane)
    print("==active==")
    print(panes._active_pane)


def enrich(txt):
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
    def __init__(self, pane_id, l1=None, l2=None, secs=2, recur=True):
        self.pane_id = pane_id
        self._disp_time = secs
        self._recurring = recur
        self._line0 = l1
        self._line1 = l2
        self.started_at = None

    def re_display(self):
        """Re-display our content on the LCD."""
        global lcd
        if self._line0:
            # Update line 1 since there is new content.
            lcd.lcd_string(enrich(self._line0), 0)
        if self._line1:
            # Update line 2 since there is new content.
            lcd.lcd_string(enrich(self._line1), 1)

    def start_display(self):
        """Display our content on the LCD."""
        self.re_display()
        self.started_at = time()  # To compute display time later

    def is_recurring(self):
        """Returns True if pane is repeating"""
        return self._recurring

    def is_done(self):
        """Returns True if pane has been displayed long enough."""
        return time() >= self.started_at + self._disp_time if self.started_at else True

    def __str__(self):
        return('pane at 0x%x(id="%s", l1="%s", l2="%s", secs=%s, recur=%s)' %
               (id(self), self.pane_id, self._line0, self._line1, self._disp_time, self._recurring))


class Panes:
    """A class to hold all our LCD panes and control displaying them."""

    def __init__(self):
        """Set-up the panes. Everything starts empty."""
        self._queue = []  # The display queue
        self._active_pane = None  # The pane currently on display
        self._panes = {}  # Definition of all panes

    def insert_update(self, pane):
        """Insert a pane, or update it if we already have it.
        Panes are identified by pane.pane_id.
        """
        pane_id = pane.pane_id
        existing_pane = self._panes.get(pane_id)

        # Insert the new definition
        self._panes[pane_id] = pane

        if existing_pane is None:
            # New pane, just queue it.
            self._queue.append(pane)
        else:
            # We need to maintain started_at time.
            pane.started_at = existing_pane.started_at

    def delete(self, id_):
        p = self._panes.pop(id_)
        try:
            self._queue.remove(p)
        except ValueError:
            # We don't have this pane.
            pass

    def lcd_tick(self):
        """Called during main loop to find out if something should happen with the LCD."""

        def display_next():
            """Helper to display some text."""
            try:
                self._active_pane = next_pane = self._panes[self._queue.pop(0).pane_id]
            except (IndexError, KeyError):
                # Nothing to do as it seems
                self._active_pane = None
                lcd.lcd_clear()
                return
            next_pane.start_display()  # Put next one on

        active_pane = self._active_pane
        if active_pane is None:
            # We are not displaying, but may have active panes. Give it a try.
            display_next()
        else:
            # We are currently displaying. Get the actual definition.
            pane = self._panes.get(active_pane.pane_id)
            if pane is None:
                # Our definition no longer exist. Stop display and get the next.
                display_next()
            elif pane is not active_pane:
                # Different pane with same ID. The started_at is maintained, so just
                # update self._active_pane and re_display
                self._active_pane = pane
                pane.re_display()
                # Deliberately ignore display time check for one tick, so we can see the change.
            elif active_pane.is_done():
                # No change, but We're done displaying
                if active_pane.is_recurring():
                    # Put it back at the end, and keep the definition
                    self._queue.append(pane)
                else:
                    # Throw away the definition
                    self._panes.pop(active_pane.pane_id)
                display_next()  # and get the next one, if any

    def execute(self, directive):
        """Get directive for a pane definition and handle it accordingly to the action given."""
        action = directive['action']
        assert action in {
            'upsert', 'delete'}, "Need an action like upsert or delete."
        pane_id = directive.get('id')
        assert pane_id and len(pane_id) > 0, 'Need an ID.'

        if action == 'upsert':
            l1 = directive.get('l1', None)
            l2 = directive.get('l2', None)
            assert l1 or l2, 'Need at least one of l1, l2'
            secs = directive.get('secs') or 2
            recur = directive.get('recur') or False
            self.insert_update(
                pane(pane_id, l1, l2, secs=secs, recur=recur)
            )
        elif action == 'delete':
            self.delete(pane_id)

    def preload(self, preload_directives):
        """Preload panes from the configuration file (if any)."""
        for directive in preload_directives:
            self.execute(directive)


# TODO priority based queuing
# TODO display background intensity
print('LCD display (axa_display.py) version 0.1 (no priority, no background intensity)')

# Get our LCD display going empty
lcd = lcd_setup()

# Set-up our panes structure and preload panes.
panes = Panes()
if 'preloads' in my_cfg:
    panes.preload(my_cfg['preloads'])

# Setup our local MQTT agent. Parameters are obtained from the ./configuration.json file.
loc_mqtt = AE_Local_MQTT()
loc_mqtt.setup()

# Open input channel for application control messages
loc_mqtt.subscribe(cfg['local_MQTT']['control_sub_tpc'], control_cb)

# Open input channel for display messages
loc_mqtt.subscribe(my_cfg['display_sub_tpc'], display_cb)

loc_mqtt.subscribe('debug', debug_cb)

while not stop_loop:
    # Check status and change display if needed.
    panes.lcd_tick()
    sleep(tick)

print('Got stop request. LCD display exits')
lcd.lcd_clear()
