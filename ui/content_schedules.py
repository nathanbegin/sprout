import time


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





def schedules_list():
    # c = load_csv('config/commands.txt')
    s = load_csv('config/user_schedule.txt')
    # z = load_csv('config/zones.txt')

    # switch the ones that should be opened
    now = (int(time.strftime("%H", time.localtime(time.time())).split(":")[0])*60) + \
        int(time.strftime("%M", time.localtime(time.time())).split(":")[0])

    # status


    ret = '''
    <div class="panel-heading">Schedules</div>
    <div class="panel-body">

        <div class="btn-group btn-group-sm" role="toolbar" aria_label="...">
        <button type="button" class="btn btn-default" style="color:#0053e3" data-toggle="modal" data-target="#add_scheduleform">
        <span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button></div>


    </div>
    <!-- Table -->
    <table class="table table-striped">
    <thead><tr><th></th><th>Zone</th><th>Duration</th><th>Start</th><th>End</th><th>Active</th><th>action</th></thead>
      '''
    for k, v in s.items():
        # Background color ON(green)/OFF(red)/inactive(grey)
        if v['active'] == '0':
            tr_class = 'class="default" style="background-color:#efeffa;color:#aaaaaa"'
            active = '<span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>'
            button_activate = '<a href="/switch_schedule?zid={}" class="btn btn-default" style="color:#0a5"><span class="glyphicon glyphicon-off" aria-hidden="true"></span></a>'.format(str(k))

        else:
            active = '<span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span></button>'
            button_activate = '<a href="/switch_schedule?zid={}" class="btn btn-default" style="color:#f55"><span class="glyphicon glyphicon-off" aria-hidden="true"></span></a>'.format(str(k))

            if convert_to_minutes(v['start']) <= now and (convert_to_minutes(str(v['start'])) + int(v['duration'])) > now:
                color = '0a5'
                tr_class = 'class="success"'
            else:
                color = 'f55'
                tr_class = 'class="danger"'


        # buttons
        button_delete = '<button type="button" class="btn btn-default" data-toggle="modal" data-target="#edit_schedform{}"><span class="glyphicon glyphicon-trash" aria-hidden="true"></span></button>'

        button_edit = '<button type="button" class="btn btn-default" style="color:#0053e3" data-toggle="modal" data-target="#edit_schedform{}"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>'

        buttons = '<div class="btn-group btn-group-sm" role="toolbar" aria_label="...">{}{}{}' \
                '</div>'.format(button_activate, button_edit, button_delete,  str(k))
               

        ret += '''<tr {}>
                    <td>#{} </td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    </tr>'''.format(tr_class,
                                 str(k),
                                 str(v['zone']),
                                 str(v['duration']),
                                 str(v['start']),
                                 str(convert_from_minutes(convert_to_minutes(str(v['start'])) + int(v['duration']))),
                                 active,
                                 buttons)

    ret += '''</table>'''
    return ret




def schedules_add_form():
    # s = load_csv('config/user_schedule.txt')
    z = load_csv('config/zones.txt')

    # switch the ones that should be opened
    now = (int(time.strftime("%H", time.localtime(time.time())).split(":")[0])*60) + \
        int(time.strftime("%M", time.localtime(time.time())).split(":")[0])

    # available ports
    zone_list = []
    zone_select = '<select class="custom-select" name="zone">'
    for k, v in z.items():
        if v['zone'] not in zone_list:
            zone_list.append(v['zone'])
            zone_select += '<option>' + str(v['zone']) + '</option>'
    zone_select += '</select>'

    button = {}
    for w in ["vpd", "sunset", "temperature", "rain", "forecast"]:
        button[w] = '''<div class="form-group">
        <label for="recipient-name" class="control-label">Modulate with {}:</label>
        <div class="btn-group" data-toggle="buttons">
          <label class="btn btn-default">
            <input type="radio" name="{}" value="1" autocomplete="off">
            <span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span> ON
          </label>
          <label class="btn btn-default active">
            <input type="radio" name="{}" value="0" autocomplete="off" checked>
            <span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span> OFF
          </label>
    </div></div>'''.format(w, w, w)


    ret = '''
    <form action="/add_schedule" method="Post">
            <div class="modal fade" id="add_scheduleform" tabindex="-1" role="dialog" aria-labelledby="add_scheduleformLabel">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="add_scheduleLabel">Add new schedule</h4>
                  </div>
                  <div class="modal-body">
                      <div class="form-group">
                        <label for="recipient-name" class="control-label">Zone:  </label>
                            {}
                      </div>
                        <div class="form-group">
                        <label for="recipient-name" class="control-label">Start time:  </label>
                            <input class="form-control" id="message-text" type="time" name="start">
                      </div>
                    <div class="form-group">
                        <label for="recipient-name" class="control-label">Duration:  </label>
                            <input class="form-control" id="message-text" name="duration">
                      </div>


                    <div class="form-group">
                        <label for="recipient-name" class="control-label">Status:</label>
                        <div class="btn-group" data-toggle="buttons">

                      <label class="btn btn-default active">
                        <input type="radio" name="active" value="1" autocomplete="off" checked>
                        <span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span> ON</label>

                      <label class="btn btn-default">
                        <input type="radio" name="active" value="0" autocomplete="off">
                        <span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span> OFF</label>
                    </div></div>


                       {}

                       {}

                       {}

                       {}

                       {}

                </div>

                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Add schedule</button>
                  </div>
                </div>
              </div>
            </div>
            </form>
    '''.format(zone_select, button['vpd'], button['temperature'], button['sunset'], button['rain'], button['forecast'])

    return ret

def add_schedule(form):
    us = load_csv('config/user_schedule.txt')
    z = load_csv('config/zones.txt')

    newrow = len(us)
    for k, v in us[0].items():
        if k == "zone":
            for kz, vz in z.items():
                if vz['zone'] == form['zone']:
                    us[newrow]['port'] = vz['port']
        elif k in form.keys():
            us[newrow][k] = form[k]
        else:
            us[newrow][k] = 0
    us[newrow]['tmp'] = '0'
    print(us[newrow])
    save_csv('config/user_schedule.txt', us)



def edit_schedule(r):
    z = load_csv('config/zones.txt')
    for k, v in z.items():
        if v['port'] == r['zid']:
            z[k]['zone'] = r['zone_name']
            z[k]['description'] = r['desc']
            if r['status'] == "active":
                z[k]['active'] = "True"
            else:
                z[k]['active'] = "False"

    save_csv('config/zones.txt', z)
    return


def schedules_edit_forms():
    z = load_csv('config/zones.txt')

    # available ports
    # get list of used ports
    ports = []
    gpio_boardports = [12, 13, 15, 16, 18, 22]
    for k, v in z.items():
        ports.append(v['port'])
    avail = [x for x in gpio_boardports if x not in set(ports)]

    ret = ''
    for k, v in z.items():
        activebutton = ("active", "checked") if v['active'] == "True" else ("", "")
        inactivebutton = ("active", "checked") if v['active'] == "False" else ("", "")
        #
        # if v['active'] == "True":
        #     activebutton = ("active", "checked")
        #     inactivebutton = ("", "")
        # else:
        #     activebutton = ("", "")
        #     inactivebutton = ("active", "checked")
        #


        ret += '''
                    <form action="/edit_zone" method="Post">

            <div class="modal fade" id="edit_zoneform{}" tabindex="-1" role="dialog" aria-labelledby="add_scheduleformLabel">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="add_scheduleLabel">Edit zone attached to port {}</h4>
                  </div>
                  <div class="modal-body">

                        <div class="btn-group" data-toggle="buttons">

                          <label class="btn btn-default {}">
                            <input type="radio" id="active" name="status" value="active" autocomplete="off" {}>
                            <span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span> Active</label>

                          <label class="btn btn-default {}">
                            <input type="radio" id="inactive" name="status" value="inactive" autocomplete="off" {}>
                            <span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span> Inactive</label>

                        </div>

                        <div class="form-group">
                            <label for="recipient-name" class="control-label">Zone name:  </label>
                            <input class="form-control" id="message-text" name="zone_name" value="{}">
                            <input name="zid" type="hidden" value="{}">
                        </div>

                      <div class="form-group">
                        <label for="message-text" class="control-label">Description:</label>
                        <input type="text" class="form-control" name='desc' value="{}">
                      </div>

                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Cancel</button>
                    <button type="submit" class="btn btn-primary">Apply</button>
                  </div>
                </div>
              </div>
            </div>
                    </form>
        '''.format(str(v['port']),str(v['port']), activebutton[0], activebutton[1], inactivebutton[0], inactivebutton[1], str(v['zone']), str(v['port']), str(v['description']))

    return ret





def switch_sched(zid):
    z = load_csv('config/user_schedule.txt')
    z[int(zid)]['active'] = "1" if z[int(zid)]['active'] == "0" else "0"
    save_csv('config/user_schedule.txt', z)
 