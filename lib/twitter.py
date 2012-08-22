from datetime import datetime
import tweepy
import lib.db as db

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_SECRET = ''

_twitter_api = None
   
def get_twitter_api():
    global _twitter_api
    if not _twitter_api:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        _twitter_api = tweepy.API(auth)
    return _twitter_api
    
def tweet(status):
    api = get_twitter_api()
    api.update_status(status)

def tweet_event(event):
    id, name, host, url = event
    status = '%s hosted by %s. #ElixirWar %s' % (name, host, url)
    tweet(status)

def get_mentions():
    api = get_twitter_api()
    mention_id = db.get_last_mention()
    if mention_id:
        return api.mentions(since_id=mention_id)
    return api.mentions()
    
