

def load_csv(myfile, header=True):
    """
    loads a CSV to a dict of dict
    """
    import collections
    with open(myfile, "r") as f:
        r = 0
        ret = collections.defaultdict(collections.OrderedDict)
        for row in f.readlines():
            if r == 0 and header is True:
                keys = list(map(lambda x: x.strip("\n"), row.split(",")))
                r = -1
                header = False
            else:
                rsplit = row.split(",")
                for i, k in enumerate(keys):
                    ret[r][k] = rsplit[i].strip("\n")

            r += 1

    return ret
def save_csv(filename, d, header=True):
    if header:
        hrow = []

        for k in d[0].keys():
            hrow.append(str(k))

        with open(filename, 'w') as f:
            f.write(",".join(hrow) + "\n")

    for row in d:
        newrow = []

        for k in d[row].keys():
            newrow.append(str(d[row][k]))

        with open(filename, 'a+') as f:
            f.write(",".join(newrow) + "\n")
def convert_from_minutes(x):
    h = str(int(x / 60))
    m = str(int(x % 60)) if int(x % 60) > 9 else "0" + str(int(x % 60))
    return h + ":" + m
def convert_to_minutes(hour):
    """

    :param hour: time ex: 18:45
    :return: 18 * 60 + 45 minutes
    """
    return int(int(hour.strip(" ").split(":")[0]) * 60 + int(hour.strip(" ").split(":")[1]))
def vpdcalc(temp, rh):
    """
    :param temp: Temperature in °C (ex: 25 for 25°C)
    :param rh: relative humidity in % (ex: 30 for 30%)
    :return: Vapour Presure Deficit (Pa)
    """
    return 610.7 * 10**((7.5 * temp) / (237.3 + temp)) * ((100 - rh) / 100)
def invert(s, inverted=True):
    """
    some (most) relays invert the signal so that they remain "off" by default.
    this function just inverts the boolean if the relay requires to
    :param s: boolean, signal
    :return: (s) if inverted is False or (not s) if inverted in True
     """
    return not s if inverted else s
