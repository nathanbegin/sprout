# Display Temp Humidity
import sys

import Adafruit_DHT
import time
import os


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


def vpdcalc(temp, rh):
    """
    :param temp: Temperature in °C (ex: 25 for 25°C)
    :param rh: relative humidity in % (ex: 30 for 30%)
    :return: Vapour Presure Deficit (Pa)
    """
    return 610.7 * 10**((7.5 * float(temp)) / (237.3 + float(temp))) * ((100 - float(rh)) / 100)


def sensor():
    sensor = Adafruit_DHT.AM2302
    pin = 24

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    humidity, temperature = str(round(humidity, 1)), str(round(temperature, 1))

    newrow = [time.strftime("%Y-%m-%d - %H:%M:%S"), temperature, humidity,
              str(round(vpdcalc(temperature, humidity), 1))]

    destfolder = os.path.join("/home", "pi", "sprout", "weatherlogs", "sensor", time.strftime("%Y"))
    destfile = os.path.join(destfolder, time.strftime("%Y-%m") + ".csv")

    if not os.path.isdir(destfolder):
        os.makedirs(destfolder)
        os.chmod(destfolder, 0o777)

    print(temperature, humidity)

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
