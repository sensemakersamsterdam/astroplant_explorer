import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


GPIO.setup(20, GPIO.OUT)
pwm = GPIO.PWM(20, 100)   # Initialize PWM on pwmPin 100Hz frequency


# main loop of program
print("\nPress Ctl C to quit \n")
dc = 0
# set dc variable to 0 (will start PWM at 0% duty cycle)
pwm.start(dc)
# Start PWM with 0% duty cycle
while True:
    # Create an infinite loop until Ctl C is pressed to stop program.
    for dc in range(0, 101, 5):
        # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.05)
# wait for .05 seconds at current LED brightness level
        print(dc)
    for dc in range(95, 0, -5):
        # Loop with dc set from 95 to 5 stepping dc down by 5 each loop
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.05)
# wait for .05 seconds at current LED brightness level
        print(dc)

pwm.stop()
GPIO.cleanup()
