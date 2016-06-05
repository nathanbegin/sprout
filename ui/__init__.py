
# create application object
from flask import Flask, request, current_app, flash, url_for, redirect
from flask import render_template
from ui import content_status, content_schedules, content_zones, content_sensor, content_wu, content_pygal
import time

app = Flask(__name__)


def log(t, ip, msg=""):
    with open("logs/requests_logs.txt", "a+") as f:
        f.write(str(t) + " - " + ip + " - " + msg + "\n")


@app.before_request
def log_request():
    if "static" not in request.url.split("/"):
        log(time.strftime("%Y-%m-%d %H:%M:%S"), request.remote_addr, msg=request.url)


@app.route('/')
@app.route('/index/')
@app.route('/schedules/')
def home():
    return render_template('index.html',
                           graph_sensor=content_pygal.graph('sensor'),
                           graph_wu=content_pygal.graph('wu'),
                           # graph_bom=content_pygal.graph('bom'),
                           schedules_active="active",
                           zones_active="",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )


@app.route('/edit_zone/', methods=['GET', 'POST'])
def edit_zone():
    content_zones.edit_zone(request.form)

    return render_template('index.html',
                           schedules_active="",
                           zones_active="active",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )


@app.route('/switch_zone/', methods=['GET'])
def switch_zone():
    content_zones.switch_zone(int(request.args.get('zid')))

    return render_template('index.html',
                           schedules_active="",
                           zones_active="active",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )


@app.route('/add_schedule', methods=['GET', 'POST'])
def add_schedule():
    content_schedules.add_schedule(request.form)

    return render_template('index.html',
                           schedules_active="active",
                           zones_active="",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )


@app.route('/switch_schedule/', methods=['GET'])
def switch_schedules():
    content_schedules.switch_sched(int(request.args.get('zid')))

    return render_template('index.html',
                           schedules_active="active",
                           zones_active="",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )


@app.route('/switch_main/', methods=['GET'])
def switch_main():
    content_zones.switch_main(int(request.args.get('zid')))

    return render_template('index.html',
                           schedules_active="",
                           zones_active="active",
                           logs_active="",
                           port_status=content_status.port_status(),
                           schedules_list=content_schedules.schedules_list(),
                           schedules_add_form=content_schedules.schedules_add_form(),
                           zones_list=content_zones.zones_list(),
                           zones_edit_forms=content_zones.zones_edit_forms(),
                           sensor=content_sensor.content_sensor(),
                           wu=content_wu.latest()
                           )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')