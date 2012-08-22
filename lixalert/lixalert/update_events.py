import mechanize
from datetime import datetime

BASEURL = "http://board.nexustk.com/ComEvents/"

def get_comm_events():
    events = []
    year = datetime.now().strftime('%Y')
    url = BASEURL + "index.html"
    br = mechanize.Browser()
    br.set_handle_refresh(False)
    br.open(url)
    for link in br.links(text_regex="[Tt][Aa][Gg]|[Ll][Ii][Xx]"):
        eventid = year + link.url.replace('.html', '')[-8:]
        host = link.url.replace('.html', '')[:-8]
        name = link.text.replace('\xa0', ' ')
        event = (eventid, name, host, BASEURL + link.url)
        events.append(event)
    return events
     
if __name__ == '__main__':
    import sys
    import lib.db as db
    import lib.twitter as twitter

    for event in get_comm_events():
        exists = db.get_event_exists(event[0])
        if exists:
            print 'Reached known events.  No new events found.  Exiting.'
        else:
            db.update_event(*event)
#            twitter.tweet_event(event)
            print 'tweeting event...', event
            db.update_user(event[2], add_flags=db.USER_FLAG_HOST)
        sys.exit()
