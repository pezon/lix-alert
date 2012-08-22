import sqlite3

SQLDB = 'db/elixirs.db'

USER_FLAG_HOST = 1
USER_FLAG_TRACK = 2
USER_FLAG_NOPROFILE = 4  
USER_FLAG_NOPROFILE_ALERTED = 8
 
def query(sql, vars=None):
    conn = sqlite3.connect(SQLDB)
    cursor = conn.cursor()
    if vars:
        cursor.execute(sql, vars)
    else:
        cursor.execute(sql)
    conn.commit()
    return cursor

def update_user(username, add_flags=0, remove_flags=0):
    sql = "insert or ignore into users (username, event_type, flags) values (?, 'elixir', 0)"
    query(sql, (username,))
    if add_flags:
        sql = "update users set tsmodified = date('now'), flags = (flags | ?) where username = ?"
        flags = int(add_flags)
        params = (flags, username)
    elif remove_flags:
        sql = "update users set tsmodified = date('now'), flags = ((flags | ?) ^ ?) where username = ?"
        flags = int(remove_flags)
        params = (flags, flags, username)
    else:
        sql = "update users set tsmodified = date('now') where username = ?"
        params = (username,)
    query(sql, params)

def update_user_record(*params):
    sql = "insert or ignore into user_records (username, event_type, won, lost, played, pct, tsadded) values (?, 'elixir', ?, ?, ?, ?, ?)" 
    q = query(sql, params)
 
def update_twitter(*params):
    sql = "insert or ignore into twitters (username, twitter_id, twitter_name) values (?, ?, ?)"
    query(sql, params)  
    params = (params[1],)
    sql = "update twitters set tsmodified = date('now') where twitter_id = ?"
    query(sql, params)

def update_twitter_mention(*params):
    sql = "insert or ignore into twitter_mentions (mention_id, twitter_id, twitter_name, mention)  values (?, ?, ?, ?)"
    query(sql, params) 
    
def update_command(*params):
    sql = "insert or ignore into twitter_commands (mention_id, username, command)  values (?, ?, ?)"
    query(sql, params)

def update_event(*params):
    sql = "insert or ignore into events (event_id, event_type, name, host, url) values (?, 'elixir', ?, ?, ?)"
    query(sql, params) 

def update_event_user(*params):
    sql = "insert or ignore into events (event_id, username, won, event_ts, record_ts) value (?, ?, ?, ?, ?)" 
    query(sql, params)

def get_tracked_users():
    flags = USER_FLAG_TRACK
    sql = "select username from users where (flags & ?) = ?"
    return query(sql, (flags, flags))

def get_event_exists(event_id):
    events = get_last_events().fetchall()
    return len(events) > 0 and str(events[0][0]) == str(event_id)
    
def get_last_events():
    sql = "select event_id, tsadded from events order by tsadded desc limit 2"
    return query(sql)

def get_last_mention():
    sql = "select max(mention_id) from twitter_mentions"
    try:
        return query(sql).fetchone()[0]
    except:
        return 0
