#!/usr/bin/python3
import time
import RPi.GPIO as GPIO
import os
import sys
import threading


def rain(pin):
    # file to log rainfall data in
    LOGFILE = os.path.join("/home","pi","sprout","weatherlogs", "rain_"+ str(pin) +".txt")

    GPIO.setmode(GPIO.BCM)  
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def rain_log(click):

        mode = "w" if not os.path.isfile(LOGFILE) else "a"
        with open(LOGFILE, mode) as f:
            f.write(str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n")
##            print(str(pin), str(time.time()))


    # register the call back for pins interrupts
    # GPIO.add_event_detect(PIN, GPIO.FALLING, callback=cb, bouncetime=300)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=rain_log, bouncetime=300)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            sys.exit()


if __name__ == "__main__":
    t1 = threading.Thread(target= rain, args=(7,))
    t1.start()

    t2 = threading.Thread(target= rain, args=(25,))
    t2.start()

                     
