import RPi.GPIO as GPIO
from inc.config import *


def port_status():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(main_valve, GPIO.OUT)
    GPIO.setup(gpio_boardports, GPIO.OUT)

    # main valve
    btn_class = "btn btn-xs btn-success" if not GPIO.input(main_valve) else "btn btn-xs btn-danger"
    output = '<button type="button" class="btn btn-xs btn-' + btn_class + '">' + str(main_valve) + '</button>'

    # other valves
    output += ' <div class="btn-group" role="group" aria-label="...">'
    for p in valves:
        btn_class = "btn btn-xs btn-success" if not GPIO.input(p) else "btn btn-xs btn-danger"
        output += '<button type="button" class="btn btn-xs btn-' + btn_class + '">' + str(p) + '</button>'


    output += '</div>'

    return output
