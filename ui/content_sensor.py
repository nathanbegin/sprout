import time
import os
from inc.functions import *
from inc.csv import *
from inc.config import *




def content_sensor():
    today = os.path.join("/home", "pi", "sprout","weatherlogs", "sensor", time.strftime("%Y"), time.strftime("%Y-%m") + ".csv")
    ret = "Temp: -, RH: -"

    if os.path.isfile(today):
        sensor = load_csv(today)
        last = max(sensor.keys())

        ret = "".join([ "<font size='16'>", sensor[last]['temp'], "&deg;C</font> - <font size='16'>", sensor[last]['rh'], "%</font> (", sensor[last]['timestamp'],")"])

    return ret