import time
import os


def load_csv(myfile, header=True):
    """
    loads a CSV to a dict of dict
    """
    import collections
    with open (myfile, "r") as f:
        r = 0
        ret = collections.defaultdict(dict)
        for row in f.readlines():
            if r == 0 and header==True:
                keys = list(map(lambda x:x.strip("\n"), row.split(",")))
                r = -1
                header = False
            else:
                rsplit = row.split(",")
                for i, k in enumerate(keys):
                   ret[r][k] = rsplit[i].strip("\n")

            r += 1

    return ret



def content_sensor():
    today = os.path.join("/home", "pi", "sprout","weatherlogs", "sensor", time.strftime("%Y-%m"), time.strftime("%Y-%m-%d") + ".csv")
    ret = "Temp: -, RH: -"

    if os.path.isfile(today):
        sensor = load_csv(today)
        last = max(sensor.keys())

        ret = "".join([sensor[last]['time'], " | Temp: ", sensor[last]['temp'], ", RH: ", sensor[last]['rh']])

    return ret