# Display Temp Humidity
import sys
import RPi.GPIO as GPIO

import Adafruit_DHT
import time
import os
from inc.functions import *
from inc.csv import *
from inc.config import *


GPIO.setmode(GPIO.BOARD)

# how to rename different columns
columns_rename = {'time': 'timestamp',
                  'tempm': 'temp',
                  'hum': 'rh',
                  'wspd': 'wind',
                  'pressurem': 'pressure',
                  'precip_ratem': 'rain_rate',
                  'dewptm': 'dewpt',
                  'air_temp': 'temp',
                  'apparent_t': 'app_temp',
                  'wind_spd_kmh': 'wind',
                  'rel_hum': 'rh',
                  'rain_trace': 'rain_9h',
                  'cloud_oktas': 'cloud',
                  'dewpt': 'dew',
                  'press_msl': 'pressure',
                  'vis_km': 'visibility',
                  'vpd': 'vpd'
                  }


def sensor():
    sensor = Adafruit_DHT.AM2302

    humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMP_SENSOR_PIN)
    humidity, temperature = str(round(humidity, 1)), str(round(temperature, 1))

    newrow = [time.strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity,
              str(round(vpdcalc(float(temperature), float(humidity)), 1))]

    destfolder = os.path.join(FOLDERS['sensor'], time.strftime("%Y"))
    destfile = os.path.join(destfolder, time.strftime("%Y-%m") + ".csv")

    if not os.path.isdir(destfolder):
        os.makedirs(destfolder)
        os.chmod(destfolder, 0o777)

    if not os.path.isfile(destfile):
        with open(destfile, "w+") as f:
            f.write("timestamp,temp,rh,vpd\n")
            f.write(",".join(newrow) + "\n")
    else:
        with open(destfile, "a+") as f:
            f.write(",".join(newrow) + "\n")

    print(time.strftime("%Y-%m-%d %H:%M:%S"), "Sensor update", temperature, humidity)


if __name__ == "__main__":
    sensor()
