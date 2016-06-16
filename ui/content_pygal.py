import os
import time
import pygal
from datetime import date, timedelta, datetime

from inc.functions import *
from inc.csv import *
from inc.config import *



def graph(what):
    """

    what = 'wu' or 'sensor'
    """
    # dates
    return

    # ext = ".txt" if what == "sensor" else ".csv"
    ext = ".csv"

    today = date.today()
    yesterday = date.today() - timedelta(1)

    print(today.strftime("%Y-%m-%d"), yesterday.strftime("%Y-%m-%d"))

    # folders
    folder = os.path.join("/home", "pi", "sprout", "weatherlogs", what)

    # files
    today_file = os.path.join(folder, today.strftime("%Y"), today.strftime("%Y-%m") + ext)
    yesterday_file = os.path.join(folder, yesterday.strftime("%Y"), yesterday.strftime("%Y-%m") + ext)
    # today_file = os.path.join(folder, '2016-06', '2016-06-01.csv')
    # yesterday_file = os.path.join(folder, '2016-05', '2016-05-31.csv')

    # load files
    # print(today_file)
    data = load_csv2(yesterday_file)

    # merge
    auj = load_csv2(today_file)
    for k in data.keys():
        data[k].extend(auj[k])

    for key in ['temp']:
        if key in data.keys():
            print(key)
            data[key] = list(map(float, data[key]))

   # return data
    # try pygal
    timestamps = []
    dat = []
    for i, ts in enumerate(data['timestamp']):
        if datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") >= ( datetime.today() - timedelta(1)):
            timestamps.append(ts)
            dat.append(data['temp'][i])
# def graph():

    # data_sensor = load_data('sensor')
    # data_bom = load_data('bom')
    # data_wu = load_data('wu')

    graph = pygal.Line()
    graph.title = what
    graph.x_labels = timestamps
    graph.add('Temperature', dat)
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
