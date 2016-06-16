#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import os
import sys


# this many mm per bucket tip
CALIBRATIONrain = 1    # mm per bucket tip
# which GPIO pin the gauge is connected to
rain_pin = 7
# file to log rainfall data in
LOGFILE = os.path.join("/home","pi","sprout","weatherlogs", "rain.txt")

GPIO.setmode(GPIO.BCM)  
GPIO.setup(rain_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# variable to keep track of how much rain
increment = 0

# the call back function for each bucket tip
def rain_log(click):

    mode = "w" if not os.path.isfile(LOGFILE) else "a"
    with open(LOGFILE, mode) as f:
        f.write(str(time.time()) + "\n")


# register the call back for pin interrupts
# GPIO.add_event_detect(PIN, GPIO.FALLING, callback=cb, bouncetime=300)
GPIO.add_event_detect(rain_pin, GPIO.RISING, callback=rain_log, bouncetime=300)





while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()