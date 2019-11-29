"""Script to show how to program LED1 intensity with Pulse Width Modulation (PWM)
"""
import RPi.GPIO as GPIO             # Import GPIO library
import astroplant_explorer as AE    # Set up GPIO for astroplat and get AE symbols
from time import sleep              # Get the sleep function


# Initialize PWM on LED1 pwmPin 100Hz frequency
pwm = GPIO.PWM(AE.LED1, 100)
pwm.start(0)   # Start PWM with 0% duty cycle

# begin main loop of program
print("\nPress Ctl-C to quit...")
try:
    # Infinite loop until Ctl C is pressed to stop program.
    while True:
        # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)
            # Wait for 0.05 s = 50 ms at current LED brightness level
            sleep(0.05)
            print(dc, end=',')
        print()

        # Loop with dc set from 95 to 5 stepping dc down by 5 each loop
        for dc in range(95, 0, -5):
            pwm.ChangeDutyCycle(dc)
            # wait for 0.05 s = 50 ms at current LED brightness level
            sleep(0.05)
            print(dc, end=',')
        print()

except KeyboardInterrupt:
    print("Ctl-c has been pressed.")
finally:
    # Shut down LED1
    pwm.stop()
    GPIO.output(AE.LED1, GPIO.LOW)
    GPIO.cleanup()
