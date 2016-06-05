import RPi.GPIO as GPIO


def port_status():
    GPIO.setmode(GPIO.BOARD)
    main_valve = 11
    gpio_boardports = [12, 13, 15, 16, 18, 22]

    GPIO.setup(main_valve, GPIO.OUT)
    GPIO.setup(gpio_boardports, GPIO.OUT)

    # main valve
    btn_class = "btn btn-xs btn-success" if not GPIO.input(11) else "btn btn-xs btn-danger"
    output = '<button type="button" class="btn btn-xs btn-' + btn_class + '">' + str(main_valve) + '</button>'

    # other valves
    output += ' <div class="btn-group" role="group" aria-label="...">'
    for p in gpio_boardports:
        btn_class = "btn btn-xs btn-success" if not GPIO.input(p) else "btn btn-xs btn-danger"
        output += '<button type="button" class="btn btn-xs btn-' + btn_class + '">' + str(p) + '</button>'


    output += '</div>'

    return output
