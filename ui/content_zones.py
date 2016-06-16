import time
from inc.functions import *
from inc.csv import *
from inc.config import *




def zones_list():
    z = load_csv('config/zones.txt')

    ret = '''
    <div class="panel panel-default">
    <div class="panel-heading">Zones</div>
    <div class="panel-body">

    <!-- Table -->
    <table class="table table-striped">
    <thead><tr><th>Port</th><th>Zone name</th><th>Zone description</th><th>Active?</th><th>Main?</th><th>action</th></thead>
    '''

    for i, row in z.items():
        # active ?
        if row['active'] == "1":
            tr_class = "success"
            active = '<span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span></button>'
            button_activate = '<a href="/switch_zone?zid={}" class="btn btn-default" style="color:#f55"><span class="glyphicon glyphicon-off" aria-hidden="true"></span></a>'.format(str(row[
                                                                                                                                                                                     'port']))

        else:
            tr_class = "danger"
            active = '<span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>'
            button_activate = '<a href="/switch_zone?zid={}"class="btn btn-default" style="color:#0a5"><span class="glyphicon glyphicon-off" aria-hidden="true"></span></a>'.format(str(row[
                                                                                                                                                                                    'port']))

        # depends on main ?
        if row['main'] == "1":
            depends_main = '<span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span></button>'
            button_main = '<a href="/switch_main?zid={}" class="btn btn-default" style="color:#f55"><span class="glyphicon glyphicon-resize-small" aria-hidden="true"></span></a>'.format(str(row[
                                                                                                                                                                                          'port']))

        else:
            depends_main = '<span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>'
            button_main = '<a href="/switch_main?zid={}"class="btn btn-default" style="color:#0a5"><span class="glyphicon glyphicon-resize-full" aria-hidden="true"></span></a>'.format(str(row[
                                                                                                                                                                                        'port']))

        buttons = '<div class="btn-group btn-group-sm" role="toolbar" aria_label="...">{}{}' \
                  '<button type="button" class="btn btn-default" style="color:#0053e3" data-toggle="modal" data-target="#edit_zoneform{}">' \
                  '<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button></div>'.format(button_activate, button_main,
                                                                                                              str(row['port']))

        ret += '''<tr class="{}">
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td>
                    <td>{}</td></tr>'''.format(tr_class,
                                               str(row['port']),
                                               str(row['zone']),
                                               str(row['description']),
                                               active,
                                               depends_main,
                                               buttons)

    # add row for buttons
    ret += '''</table></div>'''

    return ret

# def zones_add_form():
#     z = load_csv('config/zones.txt')

#     # all ports
#     gpio_boardports = [12, 13, 15, 16, 18, 22]

#     # available ports
#     # get list of used ports
#     ports = []
#     for k, v in z.items():
#         ports.append(v['port'])
#     avail = [x for x in gpio_boardports if x not in set(ports)]


#     port_list = '<select class="custom-select" name="port">'
#     for i, p in enumerate(avail):
#         port_list += '<option>' + str(p) + '</option>'
#     port_list += '</select></div>'

#     ret = '''
#     <form action="/add_zone" method="Post">
#             <div class="modal fade" id="add_zoneform" tabindex="-1" role="dialog" aria-labelledby="add_scheduleformLabel">
#               <div class="modal-dialog" role="document">
#                 <div class="modal-content">
#                   <div class="modal-header">
#                     <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
#                     <h4 class="modal-title" id="add_scheduleLabel">Add new schedule</h4>
#                   </div>
#                   <div class="modal-body">
#                     <form action="/add_zone" method="Post">
#                       <div class="form-group">
#                         <label for="recipient-name" class="control-label">Zone name:  </label>
#                             <input class="form-control" id="message-text" name="zone_name">
#                           </div>
#                       <div class="form-group">
#                         <label for="message-text" class="control-label">Port:</label>
#                        {}
#                       </div>
#                       <div class="form-group">
#                         <label for="message-text" class="control-label">Description:</label>
#                         <input type="text" class="form-control" name='desc' id="recipient-name">
#                       </div>
#                     </form>
#                   <div class="modal-footer">
#                     <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
#                     <button type="submit" class="btn btn-primary">Add zone</button>
#                   </div>
#                 </div>
#               </div>
#             </div>
#             </form>

#     '''.format(port_list)

#     return ret

# def add_zone(name, port, desc):
#     z = load_csv('config/zones.txt')

#     newrow = len(z)
#     z['zone'].append(str(name))
#     z['port'].append(str(port))
#     z['description'].append(str(desc))

#     save_csv('config/zones.txt', z)

#     output = "added zone <b>" + str(name) + "</b> (" + str(desc) + ") on port <b>" + str(port) + "</b>"
#     return output

def edit_zone(r):
    z = load_csv('config/zones.txt')
    for k, v in z.items():
        if v['port'] == r['zid']:
            z[k]['zone'] = r['zone_name']
            z[k]['description'] = r['desc']
            z[k]['main'] = r['main']
            z[k]['active'] = "1" if r['status'] == "1" else "0"

    save_csv('config/zones.txt', z)


def zones_edit_forms():
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
        activebutton = ("active", "checked") if v['active'] == "1" else ("", "")
        inactivebutton = ("active", "checked") if v['active'] == "0" else ("", "")
        mainonbutton = ("active", "checked") if v['main'] == "1" else ("", "")
        mainoffbutton = ("active", "checked") if v['main'] == "0" else ("", "")

        ret += '''<form action="/edit_zone" method="Post">
            <div class="modal fade" id="edit_zoneform{}" tabindex="-1" role="dialog" aria-labelledby="add_scheduleformLabel">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="add_scheduleLabel">Edit zone attached to port {}</h4>
                  </div>
                  <div class="modal-body">

                        <div class="form-group" data-toggle="buttons">
                          <label class="btn btn-default {}">
                            <input type="radio" id="active" name="status" value="1" autocomplete="off" {}>
                            <span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span> Active</label>
                          <label class="btn btn-default {}">
                            <input type="radio" id="inactive" name="status" value="0" autocomplete="off" {}>
                            <span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span> Inactive</label>
                        </div>

                        <div class="form-group" data-toggle="buttons">
                        <label for="recipient-name" class="control-label">Attached to main valve:  </label>
                          <label class="btn btn-default {}">
                            <input type="radio" id="main_on" name="main" value="1" autocomplete="off" {}>
                            <span style="color:#0a5" class="glyphicon glyphicon-ok" aria-hidden="true"></span> On</label>
                          <label class="btn btn-default {}">
                            <input type="radio" id="main_off" name="main" value="0" autocomplete="off" {}>
                            <span style="color:#f55" class="glyphicon glyphicon-remove" aria-hidden="true"></span> Off</label>
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
        '''.format(str(v['port']), str(v['port']),
                   activebutton[0], activebutton[1],
                   inactivebutton[0], inactivebutton[1],
                   mainonbutton[0], mainonbutton[1],
                   mainoffbutton[0], mainoffbutton[1],
                   str(v['zone']), str(v['port']), str(v['description']))

    return ret


def switch_zone(zid):
    z = load_csv('config/zones.txt')
    us_active = "1"
    for k, v in z.items():
        if int(v['port']) == int(zid):
            if v['active'] == '0':
                z[k]['active'] = "1"
                us_active = "1"
            else:
                z[k]['active'] = "0"
                us_active = "0"
    save_csv('config/zones.txt', z)

    # activate/de-activate all the schedules from that zone
    us = load_csv('config/user_schedule.txt')
    for k, v in us.items():
        if int(v['zone']) == int(zid):
            us[k]['active'] = us_active
    save_csv('config/user_schedule.txt', us)


def switch_main(zid):
    z = load_csv('config/zones.txt')
    for k, v in z.items():
        if int(v['port']) == int(zid):
            z[k]['main'] = "1" if v['main'] == "0" else "0"
    save_csv('config/zones.txt', z)
