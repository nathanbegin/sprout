#!/bin/bash


#create a bunch of useful directories
sudo mkdir -p /home/pi/sprout/logs
sudo chmod 777 /home/pi/sprout/logs
sudo mkdir -p /home/pi/sprout/config
sudo chmod 777 /home/pi/sprout/config
sudo mkdir -p /home/pi/sprout/weatherlogs/wu
sudo chmod 777 /home/pi/sprout/weatherlogs/wu
sudo mkdir -p /home/pi/sprout/weatherlogs/bom
sudo chmod 777 /home/pi/sprout/weatherlogs/bom
sudo mkdir -p /home/pi/sprout/weatherlogs/sensor
sudo chmod 777 /home/pi/sprout/weatherlogs/sensor

#create log files
sudo touch /home/pi/sprout/logs/history.log
sudo touch /home/pi/sprout/logs/server.log

# add autostart commands to crontab
#server launcher
command="sudo sh /home/pi/launcher.sh"
job="@reboot $command >> /home/pi/sprout/logs/server.log 2>&1"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job") | crontab -

#irrigation
command="sudo python3 /home/pi/sprout/irrigation.py"
job="* * * * * $command >> /home/pi/sprout/logs/history.log 2>&1"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job")| crontab -

#weather underground
command="sudo python3 /home/pi/sprout/weather.py"
job="0 * * * * $command >> /home/pi/sprout/logs/history.log 2>&1"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job")| crontab -

#sensor logging
command="sudo python3 /home/pi/sprout/sensor.py"
job="*/5 * * * * $command >> /home/pi/sprout/logs/history.log 2>&1"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job")| crontab -

#commands convert
command="sudo python3 /home/pi/sprout/convert.py"
job="0 * * * * $command >> /home/pi/sprout/logs/history.log 2>&1"
cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job")| crontab -
