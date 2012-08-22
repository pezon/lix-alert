import lib.twitter as twitter
import lib.db as db

VALID_COMMANDS = ('track', 'untrack')

for m in twitter.get_mentions():
    print 'MENTION:', m.id, m.user.id, m.user.screen_name, m.text
    try:
        commands = m.text.split()
        command = commands[1]
        username = commands[2]

        db.update_twitter(username, m.user.id, m.user.screen_name)
        db.update_twitter_mention(m.id, m.user.id, m.user.screen_name, m.text)

        if command in VALID_COMMANDS:
            print '%sing %s' % (command, username)
            db.update_command(m.id, username, command)

            if command == 'track':
                db.update_user(username, add_flags=db.USER_FLAG_TRACK)
            elif command == 'untrack':
                db.update_user(username, remove_flags=db.USER_FLAG_TRACK)
                
    except Exception, e:
        print 'error', e
        pass

