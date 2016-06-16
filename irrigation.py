#!/usr/bin/python3
import time
start= time.time()

import os
import RPi.GPIO as GPIO
import sys
import collections

from inc.functions import *
from inc.csv import *
from inc.config import *



# variables
opened = []   # list of ports that should be in opened state right now
to_delete = []  # list of expired temporary schedules that should be deleted now from user_schedule
main_dependant = []  # list of ports which are linked to the main valve
now = convert_to_minutes(time.strftime("%H:%M"))
inverted = True
GPIO.setwarnings(False)




def convert():
    commands = collections.defaultdict(dict)

    # load user_schedule
    if os.path.isfile(user_schedfile):
        us = load_csv(user_schedfile)
        z = load_csv(zonesfile)

        #create commands dictcommands = collections.defaultdict(dict)

        #loop through user_schedules file
        for k, v in us.items():
            # make a list of expired temporary schedules
            if now > (convert_to_minutes(v['start']) + int(v['duration'])) and v['tmp'] == '1':
                to_delete.append(k)

            elif v['active'] == "1":
                commands[k]['port'] = v['zone']
                commands[k]['start'] = convert_to_minutes(v['start'])
                duration = int(v['duration'])
                commands[k]['end'] = commands[k]['start'] + duration
                commands[k]['tmp'] = v['tmp']

                # look for zone infos to know if depends on main valve or not
                for kz, vz in z.items():
                    if vz['port'] == v['zone']:
                        commands[k]['main'] = vz['main']


        # delete expired schedules
        for i in to_delete:
            del us[i]  # delete from user_schedule file

        # print(us)

        # save new user_schedule file
        save_csv(user_schedfile, us)  

        return commands



def irrigation(inverted=True):


    # set GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_boardports, GPIO.OUT)

    # convert user_schedule to commands dict
    commands = convert()


    # set schedule
    for k, v in commands.items():
        # check if schedule depends on main valve 
        if v['main'] == "1":
            main_dependant.append(int(v['port']))




        if now >= int(v['start']) and now < int(v['end']):  # GPIO should be opened
            opened.append(int(v['port']))

    # loop for individual valves
    for v in valves:
        print(v,  invert(GPIO.input(v), inverted))
        if v in opened:
            if not invert(GPIO.input(v), inverted):  # the valve was closed before
                GPIO.output(v, invert(True, inverted))  # let's open it !
                with open(logfile, "a+") as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S') +
                            ",open," + str(v) + "\n")
                    print(time.strftime('%Y-%m-%d %H:%M:%S') + ",open," + str(v) + "\n")
        else:
            if invert(GPIO.input(v), inverted):  # the valve was opened before
                GPIO.output(v, invert(False, inverted))  # let's close it
                with open(logfile, "a+") as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S') +
                            ",close," + str(v) + "\n")
                    print(time.strftime('%Y-%m-%d %H:%M:%S') + ",close," + str(v) + "\n")

    # open main valve
    if len([x for x in main_dependant if x in opened]) > 0:
        # main valve was closed. we need to open it
        if not invert(GPIO.input(main_valve), inverted):
            GPIO.output(main_valve, invert(True, inverted))
            with open(logfile, "a+") as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S') +
                        ",open main," + str(main_valve) + "\n")
                print(time.strftime('%Y-%m-%d %H:%M:%S') + ",open main," + str(main_valve) + "\n")
    else:
        if invert(GPIO.input(main_valve), inverted):
            GPIO.output(main_valve, invert(False, inverted))
            with open(logfile, "a+") as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S') +
                        ",close main," + str(main_valve) + "\n")
                print(time.strftime('%Y-%m-%d %H:%M:%S') + ",close main," + str(main_valve) + "\n")

    # create status file
    with open(statusfile, "w") as f:
        f.write("port,status\n")
        for p in gpio_boardports:
            f.write(str(p) + "," + str(invert(GPIO.input(p))) + "\n")
            # print(str(p) + "," + str(invert(GPIO.input(p))) + "\n")


    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     GPIO.cleanup()


if __name__ == "__main__":
    irrigation(inverted=True)
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "Irrigation update in", time.time() - start ,"sec")
