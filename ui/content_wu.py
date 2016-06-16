import time
import os

from inc.functions import *
from inc.csv import *
from inc.config import *





def latest():
    f = os.path.join("/home", "pi", "sprout","weatherlogs", "wu", time.strftime("%Y"), time.strftime("%Y-%m") + ".csv")
    ret = "Temp: -, RH: -"

    if os.path.isfile(f):
        wu = load_csv(f)
        last = max(wu.keys())

        ret = "".join(["<font size='12'>", wu[last]['temp'], "&deg;C</font>",
            "   <font size='12'>", wu[last]['rh'], "%</font>",
            "   <font size='12'>", wu[last]['rain_rate'], "mm/h </font>", 
            "   (", wu[last]['timestamp'],")"])

      
    else:
        ret = ["file not found:" + f]
    
    return ret