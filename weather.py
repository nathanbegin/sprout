import time
import requests
import os
import numpy as np
import pandas as pd
from datetime import date, timedelta
from inc.functions import *
from inc.csv import *
from inc.config import *


# how to rename different columns
columns_rename = {'time': 'timestamp',
                  'tempm': 'temp',
                  'hum': 'rh',
                  'wspd': 'wind',
                  'pressurem': 'pressure',
                  'precip_ratem': 'rain_rate',
                  'dewptm': 'dew',
                  'air_temp': 'temp',
                  'apparent_t': 'app_temp',
                  'wind_spd_kmh': 'wind',
                  'wspdm': 'wind',
                  'rel_hum': 'rh',
                  'rain_trace': 'precip_9',
                  'cloud_oktas': 'cloud',
                  'dewpt': 'dew',
                  'press_msl': 'pressure',
                  'vis_km': 'visibility',
                  'vpd': 'vpd'
                  }
# dates
today = date.today()
today_folder, today_csv = today.strftime("%Y"), today.strftime("%Y-%m") + '.csv'

yesterday = date.today() - timedelta(1)
yesterday_folder, yesterday_csv = yesterday.strftime("%Y"), yesterday.strftime("%Y-%m") + '.csv'




def bom():
    # vars
    folder = os.path.join("/home", "pi", "sprout", "weatherlogs", "bom")
    current_month = pd.to_datetime(date(int(today.strftime("%Y")), int(today.strftime("%m")), 1))
    current_day = pd.to_datetime(date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))))
    current_yesterday = pd.to_datetime(
        date(int(today.strftime("%Y")), int(today.strftime("%m")), int(today.strftime("%d"))))

    # create folder
    for fold in [os.path.join(folder, today_folder), os.path.join(folder, yesterday_folder)]:
        if not os.path.isdir(fold):
            os.makedirs(fold)
            os.chmod(fold, 0o777)
            print("created folder:", fold)

    # download data from BOM
    df = pd.DataFrame(pd.read_json('http://www.bom.gov.au/fwo/IDN60801/IDN60801.94926.json')['observations']['data'])

    # add timestamp
    df['timestamp'] = pd.to_datetime(df.local_date_time_full, format="%Y%m%d%H%M%S")
    df.set_index('timestamp', inplace=True)

    # subset dataframe
    df = df[['air_temp',
             'apparent_t',
             'wind_spd_kmh',
             'rel_hum',
             'rain_trace',
             'cloud_oktas',
             'dewpt',
             'press_msl',
             'vis_km']]

    # reverse and resample
    df = df.iloc[::-1]
    if int(pd.__version__.split('.')[1]) >= 18:
        df2 = df.resample('1H').mean().bfill()
        df2.loc[:, 'rain_trace'] = df.resample(rule='1H').last().ffill()

    else:
        df2 = df.resample(rule='1H', how='mean', fill_method='backfill')
        df2.loc[:, 'rain_trace'] = df.rain_trace.resample(rule='1H', how='first', fill_method='pad')
    df = df2

    # transform from rain since 9am to rain since 0am
    df['rain_rate'] = df.rain_trace.apply(float).diff().fillna(0)
    df.loc[df2.rain_rate < 0, 'rain_rate'] = df.loc[df.rain_rate < 0, 'rain_trace']

    # rename columns

    df = df.rename(columns=columns_rename)

    # replace missing data
    df = df.replace({'-': np.nan}).fillna(method='bfill')

    # make sure all the numeric are indeed numeric
    # for c in ['temp', 'app_temp', 'wind', 'rh', 'rain_rate', 'rain_trace', 'cloud', 'dew', 'press', 'vis']:
    df = df.applymap(float)

    # add vpd
    df['vpd'] = vpdcalc(df['temp'], df['rh'])

    # round all values
    df = df.applymap(lambda x: round(x, 2))

    # today and yesterday
    today_data = df.loc[df.index >= current_day, :]
    yesterday_data = df.loc[(current_yesterday <= df.index) & (df.index < current_day), :]

    # changed month
    if yesterday_csv != today_csv:

        # load existing dataframe for this month
        if os.path.isfile(os.path.join(folder, yesterday_folder, yesterday_csv)):
            yesterday_monthly = pd.read_csv(os.path.join(folder, yesterday_folder, yesterday_csv))
            yesterday_monthly['timestamp'] = pd.to_datetime(yesterday_monthly.timestamp)
            yesterday_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            yesterday_monthly = pd.DataFrame()

        if os.path.isfile(os.path.join(folder, today_folder, today_csv)):
            today_monthly = pd.read_csv(os.path.join(folder, today_folder, today_csv))
            today_monthly['timestamp'] = pd.to_datetime(today_monthly.timestamp)
            today_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            today_monthly = pd.DataFrame()

        # concatenate existing data with new data
        yesterday_monthly = pd.concat([yesterday_monthly, yesterday_data]).drop_duplicates()
        yesterday_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        yesterday_monthly = yesterday_monthly.rename(columns=columns_rename)

        # remove any data from current month and keep only data from previous month
        yesterday_monthly = today_monthly.loc[today_monthly.index < current_month, :]

        # save to csv
        yesterday_monthly.to_csv(os.path.join(folder, yesterday_folder, yesterday_csv), index=False)

        # concatenate existing data with new data
        today_monthly = pd.concat([today_monthly, today_data]).drop_duplicates()
        today_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        today_monthly = today_monthly.rename(columns=columns_rename)

        # remove any data from previous month
        today_monthly = today_monthly.loc[today_monthly.index >= current_month, :]

        # save to csv
        today_monthly.to_csv(os.path.join(folder, today_folder, today_csv), index=True)

    # today and yesterday are same month
    else:
        if os.path.isfile(os.path.join(folder, today_folder, today_csv)):
            today_monthly = pd.read_csv(os.path.join(folder, today_folder, today_csv))
            today_monthly['timestamp'] = pd.to_datetime(today_monthly.timestamp)
            today_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            today_monthly = pd.DataFrame()

        # concatenate existing data with new data
        today_monthly = pd.concat([today_monthly, yesterday_data, today_data]).drop_duplicates()
        today_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        today_monthly = today_monthly.rename(columns=columns_rename)

        # remove any data from previous month
        today_monthly = today_monthly.loc[today_monthly.index >= current_month, :]

        # save csv
        today_monthly.to_csv(os.path.join(folder, today_folder, today_csv), index=True)

    # last 24h
    last24h = df.ix[-24:, :]
    last24h.to_csv(os.path.join(folder, "last24h.csv"))


def wunder_query(WUkey='33baa1312f9c6922', WUstationID='IAUSTRAL68', WUfeature='yesterday'):
    """
    :param WUkey: Weather Underground API key
    :param WUstationID: Station ID
    :param WUfeature: Feature (yesterday, history, forecast, sunset ...)
    :return: json query
    """
    WUaddress = 'http://api.wunderground.com/api/' + \
                WUkey + '/' + WUfeature + '/conditions/q/pws:' + WUstationID + '.json'
    r = requests.get(WUaddress)
    return r.json()


def extract_data(data, cols):
    """
    Puts WU json data into a dataframe
    :param data: Weather underground json data
    :param cols: cols to copy to dataframe
    :return: dataframe + resampled dataframe (1h)
    """

    df = pd.DataFrame(columns=cols)

    for i in data['history']['observations']:
        row = []
        for c in cols:
            if c == 'vpd':
                row.append(round(vpdcalc(float(i['tempm']), float(i['hum'])), 0))
            elif c == 'timestamp':
                row.append(str(i['date']['year']) + "-" + str(i['date']['mon']) + "-" + str(i['date']['mday']) + " " +
                           str(i['date']['hour']) + ":" + str(i['date']['min']) + ":00")
            else:
                row.append(i[c])
        df.loc[len(df.index) + 1, :] = row

    # rename columns
    df = df.rename(columns=columns_rename)

    # make datetimeIndex to resample
    df['timestamp'] = pd.to_datetime(df.timestamp)
    df.set_index('timestamp', drop=True, inplace=True)
    df = df.applymap(float)

    if int(pd.__version__.split('.')[1]) >= 18:
        df1h = df.resample(rule='1H').mean().bfill()
    else:
        df1h = df.resample(rule='1H', how='mean', fill_method='backfill')

    return df, df1h


def wunderground():

    #  vars
    cols = ['timestamp', 'tempm', 'hum', 'wspdm', 'pressurem', 'precip_ratem', 'dewptm', 'vpd']
    folder = os.path.join("/home", "pi", "sprout", "weatherlogs", "wu")
    current_month = pd.to_datetime(date(int(today.strftime("%Y")), int(today.strftime("%m")), 1))

    # create folder
    for fold in [os.path.join(folder, today_folder), os.path.join(folder, yesterday_folder)]:
        if not os.path.isdir(fold):
            os.makedirs(fold)
            os.chmod(fold, 0o777)
            print("created folder:", fold)

    # load data from WU
    today_data, today1h = extract_data(wunder_query(WUfeature='history'), cols)
    yesterday_data, yesterday1h = extract_data(wunder_query(WUfeature='yesterday'), cols)

    # changed month
    if yesterday_csv != today_csv:

        # load existing dataframe for this month
        if os.path.isfile(os.path.join(folder, yesterday_folder, yesterday_csv)):
            yesterday_monthly = pd.read_csv(os.path.join(folder, yesterday_folder, yesterday_csv))
            yesterday_monthly['timestamp'] = pd.to_datetime(yesterday_monthly.timestamp)
            yesterday_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            yesterday_monthly = pd.DataFrame()

        if os.path.isfile(os.path.join(folder, today_folder, today_csv)):
            today_monthly = pd.read_csv(os.path.join(folder, today_folder, today_csv))
            today_monthly['timestamp'] = pd.to_datetime(today_monthly.timestamp)
            today_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            today_monthly = pd.DataFrame()

        # concatenate existing data with new data
        yesterday_monthly = pd.concat([yesterday_monthly, yesterday_data]).drop_duplicates()
        yesterday_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        yesterday_monthly = yesterday_monthly.rename(columns=columns_rename)

        # remove any data from current month and keep only data from previous month
        yesterday_monthly = today_monthly.loc[today_monthly.index < current_month, :]

        # save to csv
        yesterday_monthly.to_csv(os.path.join(folder, yesterday_folder, yesterday_csv), index=False)

        # concatenate existing data with new data
        today_monthly = pd.concat([today_monthly, today_data]).drop_duplicates()
        today_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        today_monthly = today_monthly.rename(columns=columns_rename)

        # remove any data from previous month
        today_monthly = today_monthly.loc[today_monthly.index >= current_month, :]

        # save to csv
        today_monthly.to_csv(os.path.join(folder, today_folder, today_csv), index=True)

    # today and yesterday are same month
    else:

        if os.path.isfile(os.path.join(folder, today_folder, today_csv)):
            today_monthly = pd.read_csv(os.path.join(folder, today_folder, today_csv))
            today_monthly['timestamp'] = pd.to_datetime(today_monthly.timestamp)
            today_monthly.set_index('timestamp', drop=True, inplace=True)
        else:
            today_monthly = pd.DataFrame()

        # concatenate existing data with new data
        today_monthly = pd.concat([today_data, yesterday_data, today_monthly]).drop_duplicates()
        today_monthly.sort_index(ascending=True, inplace=True)

        # rename columns
        today_monthly = today_monthly.rename(columns=columns_rename)

        # remove any data from previous month
        today_monthly = today_monthly.loc[today_monthly.index >= current_month, :]

        # save csv
        today_monthly.to_csv(os.path.join(folder, today_folder, today_csv), index=True)

    # save the last 24h
    alldf = pd.concat([yesterday1h, today1h])
    last24h = alldf[alldf.index >= yesterday.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M:%S")]
    last24h.reset_index().to_csv(os.path.join(folder, "last24h.csv"), index=True)


def wu_sunset():
    WUastro = wunder_query(WUfeature='astronomy')

    sunsetfile = os.path.join("weatherlogs", "sunset.txt")

    sunrise, sunset = (int(WUastro['sun_phase']['sunrise']['hour']) * 60) + int(WUastro['sun_phase']['sunrise']['minute']),\
                      (int(WUastro['sun_phase']['sunset']['hour']) * 60) + int(WUastro['sun_phase']['sunset']['minute'])

    with open(sunsetfile, "w") as f:
        f.write(str(sunrise) + "," + str(sunset))


def find_nearby_stations(lat='-35.260605', long='149.111969', n=10, max_dist=10):
    WUaddress = 'http://api.wunderground.com/api/33baa1312f9c6922/geolookup/q/' + lat + ',' + long + '.json'
    r = requests.get(WUaddress)

    sids = []
    i = 0
    for s in r.json()['location']['nearby_weather_stations']['pws']['station'][:n]:
        i += 1
        if s['distance_km'] < max_dist:
            sids.append(s['id'])
    with open("nearby_stations.txt", "w") as f:
        f.write(",".join(sids))


if __name__ == "__main__":
    start = time.time()
    wunderground()
    bom()
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "Weather update")
