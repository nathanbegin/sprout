import os
import time



# files / folders
FOLDERS = {}
FOLDERS['sprout'] = os.path.join("/home", "pi", "sprout")
FOLDERS['logs'] = os.path.join(FOLDERS['sprout'], "logs")
FOLDERS['config'] = os.path.join(FOLDERS['sprout'], "config")
FOLDERS['weatherlogs'] = os.path.join(FOLDERS['sprout'], "weatherlogs")
FOLDERS['wu'] = os.path.join(FOLDERS['weatherlogs'], 'wu')
FOLDERS['bom'] = os.path.join(FOLDERS['weatherlogs'], 'bom')
FOLDERS['sensor'] = os.path.join(FOLDERS['weatherlogs'], 'sensor')

user_schedfile = os.path.join(FOLDERS['config'], "user_schedule.txt")
zonesfile = os.path.join(FOLDERS['config'], "zones.txt")
logfile = os.path.join(FOLDERS['logs'], time.strftime('%Y%m') + "_logs.txt")
statusfile = os.path.join(FOLDERS['config'], "status.txt")

# sunsetfile = os.path.join(SPROUT_FOLDER,"weatherlogs", "sunset.txt")
# weather_logfolder = os.path.join(SPROUT_FOLDER,"weatherlogs", "wu", time.strftime("%Y-%m"))
# weather_logfile = os.path.join(weather_logfolder, "last24h.csv")



# variables
gpio_boardports = [11, 12, 13, 15, 8, 10, 16]
main_valve = gpio_boardports[0]
valves = gpio_boardports[1:]
TEMP_SENSOR_PIN = 24



#Weather underground
WUstationID = ''  # closest weather station.
WUkey='33baa1312f9c6922' # WU API key




# check folders
for f, fold in FOLDERS.items():
    if not os.path.isdir(fold):
        os.makedirs(fold)
        os.chmod(fold, 0o777)