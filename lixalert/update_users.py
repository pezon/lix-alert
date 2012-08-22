##
#

# profiles update about every 3 hours
#

import mechanize
from dateutil import parser
import lib.db as db

def get_ntk_profile(username):
    url = "http://users.nexustk.com/?name=%s" % username
    br = mechanize.Browser()
    br.set_handle_refresh(False)
    response = br.open(url)
    data = response.read().lower()
    if 'We are sorry' in data:
        return None
    # profile stats
    elixirs_won = 0
    elixirs_won_last = None
    elixirs_played = 0
    for line in data.split('</td>'):
        if 'elixir' in line.lower() and 'font' in line.lower():
            line = line.lower().split('>')[2].split('<')[0]
            if 'participated' in line.lower():
                elixirs_played = int(line.split('elixir')[0].split('in')[1])
                elixirs_won_last = False
            if 'victories' in line.lower():
                elixirs_won = int(line.split('elixir')[0])
                elixirs_won_last = True
    # last modified
    datetime = ''
    for line in data.split('center>'):
        if 'last updated' in line:
            line = line.strip().split(':', 1)[1].split('\n')[0]
            datetime = parser.parse(line).strftime('%Y-%m-%d %H:%M')
    return (elixirs_won, elixirs_played, elixirs_won_last, datetime)

if __name__ == '__main__':

    events = db.get_last_events().fetchall()
    print events
    curr_event = events[0][0]
    curr_event_time = parser.parse(events[0][1])
    try:
        last_event = events[1][0]
        last_event_time = parser.parse(events[1][1])
    except:
        pass

    users = db.get_tracked_users()
    for user in users:
        username = user[0]
        profile = get_ntk_profile(username)
        if not profile:
        #    db.update_user(username, add_flags=db.USER_FLAG_NOPROFILE)
            continue

        db.update_user(username)
        db.update_user_record(username, profile[0], profile[1] - profile[0], profile[1], 1.0 * profile[0] / profile[1], profile[3])
        #db.update_event_user(curr_event, username, profile[2], curr_event_time, profile[3])
