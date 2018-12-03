#!/usr/bin/env python
from TwitterAPI import TwitterAPI
import sched
import time

# You can put any Twitter handle here, and pre-populate the tweet with any text
SCREEN_NAME = 'realDonaldTrump'
TWEET_TEXT = '@realDonaldTrump'
# You have to go to apps.twitter.com and generate these oAuth keys for your acc
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

api = TwitterAPI(CONSUMER_KEY,
                 CONSUMER_SECRET,
                 ACCESS_TOKEN_KEY,
                 ACCESS_TOKEN_SECRET)

schdlr = sched.scheduler(time.time, time.sleep)

usr_timeln_rqst = api.request('statuses/user_timeline',
                              {'screen_name': SCREEN_NAME,
                               'count': 1})
for item in usr_timeln_rqst:
        previous_tweet = item['id']


def stop_tweeting():
    def tweet_gif(sc):
        global last_tweet
        global previous_tweet

        usr_timeln_rqst = api.request('statuses/user_timeline',
                                      {'screen_name': SCREEN_NAME,
                                       'count': 1})

        for item in usr_timeln_rqst:
            last_tweet = item['id']
            if last_tweet == previous_tweet:
                print("no new tweet")
            else:
                previous_tweet = last_tweet
                file = open('./stoppls.gif', 'rb')
                data = file.read()
                media_upld_rqst = api.request('media/upload', '',
                                              {'media': data})
                print('UPLOAD MEDIA SUCCESS' if media_upld_rqst.status_code ==
                      200 else 'UPLOAD MEDIA FAILURE')
                media_id = media_upld_rqst.json()['media_id_string']
                status_upd_rqst = api.request('statuses/update',
                                              {'status': TWEET_TEXT,
                                               'media_ids': media_id,
                                               'in_reply_to_status_id':
                                               last_tweet,
                                               'auto_populate_reply_metadata':
                                               True})
                print('UPDATE STATUS SUCCESS' if status_upd_rqst.status_code ==
                      200 else 'UPDATE STATUS FAILURE')

        schdlr.enter(10, 1, tweet_gif, (sc,))

    schdlr.enter(10, 1, tweet_gif, (schdlr,))
    schdlr.run()


# I had to do this in a weird way, because the TwitterAPI often
# throws errors, this waits a minute before trying again
def try_tweeting():
    try:
        stop_tweeting()

    except Exception as e:
        time.sleep(60)
        try_tweeting()
        print(e)


try_tweeting()
