"""Basic set-up and definitions for the Astroplant Explorer kit.
"""
import RPi.GPIO as GPIO
import astroplant_explorer as AE

# Configure standard settings for the GPIO system.
GPIO.setmode(GPIO.BCM)      # BCM Mode -> pin nr == GPIO nr
GPIO.setwarnings(False)     # Disable the warnings

### Switches
# Define switch PINs
SW1 = 5                     # On GPIO5 we connect switch nr ??
# Initialize switches
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull_up

### LEDs
# Define LED pins
LED1 = 20                   # On GPIO20 we connect a LED
# Initialize LEDs
GPIO.setup(LED1, GPIO.OUT)  # Output


### Relays
# Define Relay pins
RY1 = 16                   # On GPIO16 we connect Relay 1
# Initialize Relays
GPIO.setup(RY1, GPIO.OUT)  # Output
