import time
import os
import pygal
from datetime import date, timedelta


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
                    ret[i][k] = rsplit[i].strip("\n")

            r += 1

    return ret


def load_csv2(myfile, header=True):
    """
    loads a CSV to a dict of dict
    """
    import collections
    with open(myfile, "r") as f:
        r = 0
        ret = collections.defaultdict(list)
        for row in f.readlines():
            if r == 0 and header is True:
                keys = list(map(lambda x: x.strip("\n"), row.split(",")))
                r = -1
                header = False
            else:
                rsplit = row.split(",")
                for i, k in enumerate(keys):
                    ret[k].append(rsplit[i].strip("\n"))

            r += 1

    return ret


def graph(what):
    """

    what = 'wu' or 'sensor'
    """
    # dates

    # ext = ".txt" if what == "sensor" else ".csv"
    ext = ".csv"

    today = date.today()
    yesterday = date.today() - timedelta(1)

    print(today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))

    # folders
    folder = os.path.join("/home", "pi", "sprout", "weatherlogs", what)

    # files
    today_file = os.path.join(folder, today.strftime("%Y-%m"), today.strftime("%Y-%m-%d") + ext)
    yesterday_file = os.path.join(folder, yesterday.strftime("%Y-%m"), yesterday.strftime("%Y-%m-%d") + ext)
    # today_file = os.path.join(folder, '2016-06', '2016-06-01.csv')
    # yesterday_file = os.path.join(folder, '2016-05', '2016-05-31.csv')

    # load files
    # print(today_file)
    data = load_csv2(yesterday_file)
    auj = load_csv2(today_file)

    # merge
    for k in data.keys():
        data[k].extend(auj[k])

    for key in ['pressurem', 'dewptm', 'precip_ratem', 'vpd', 'wspdm', 'hum', 'tempm','temp','rh']:
        if key in data.keys():
        	data[key] = list(map(float, data[key]))

    # return data
    # try pygal


# def graph():

    varnames = {'temperature': {'wu': 'tempm', 'bom': 'temp', 'sensor': 'temp'},
                'rh': {'wu': 'hum', 'bom': 'rh', 'sensor': 'rh'},
                'time': {'wu': 'timestamp', 'bom': 'timestamp', 'sensor': 'time'},
                }

    # data_sensor = load_data('sensor')
    # data_bom = load_data('bom')
    # data_wu = load_data('wu')

    graph = pygal.Line()
    graph.title = 'Temperatures'
    graph.x_labels = data[varnames['time'][what]]
    graph.add('Temperature', data[varnames['temperature'][what]])
    # graph.add('bom', data[varnames['temperature']['bom']])
    # graph.add('sensor', data[varnames['temperature']['sensor']])
    # graph.add('hum',  data['hum'])
    # graph.add('dewpt',  data['dewpt'])
    # graph.add('precip_ratem', data['precip_ratem'])
    # graph.add('pressurem',  data['pressurem'])
    # graph.add('vpd',  data['vpd'])
    graph_data = graph.render_data_uri()
    # graph.render_in_browser()
    return graph_data
