import datetime
import sys
import tweepy
import json
import pdb
import random

import api
import scrapey


class TwitterAPI:
    def __init__(self):
        auth = tweepy.OAuthHandler(api.consumer_key,
                                   api.consumer_secret)
        auth.set_access_token(api.access_token,
                              api.access_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

    def update_profile_pic(self, pic):
        self.api.update_profile_image(pic)

    def update_bg_pic(self, pic):
        self.api.update_profile_background_image(pic)

    def get_recent_tweets(self):
        statuses = self.api.user_timeline("guantanamobot")
        return statuses


def should_i_tweet(recent):
    timestamp = datetime.datetime.now()
    deltat = timestamp - recent[len(recent)-1].created_at

    # Let's tweet roughly every few days
    if deltat.days < random.randrange(2, 6):
        return False
    else:
        return True


def check_recent_prisoners(proposed, recent):
    tweet_text = []
    for each in range(len(recent)):
        tweet_text.append(recent[each].text)

    if proposed in recent:
        return False
    else:
        return True


def get_prisoners():
    # Get most recent scraped data
    with open('prisoners.json') as prisoner_file:
        prisoners = json.load(prisoner_file)

    timestamp = datetime.datetime.now()
    deltat = timestamp - datetime.datetime.strptime(
        prisoners["time_scraped"], "%Y-%m-%dT%H:%M:%S.%f")

    if deltat.days < 10:
        pass
    else:
        scrapey.main()
        with open("prisoners.json") as prisoner_file:
            prisoners = json.load(prisoner_file)

    prisoners.pop("time_scraped", None)
    return prisoners


def main():
    twitter = TwitterAPI()
    prisoners = get_prisoners()
    recent = twitter.get_recent_tweets()

    if not should_i_tweet(recent):
        sys.exit()

    while True:
        selected_prisoner = random.choice(list(prisoners))
        proposed = prisoners[selected_prisoner]["tweet"]

        try:
            proposed = proposed.rstrip(".")
        except:
            pass

        try:
            proposed = proposed.replace("one months", "one month")
        except:
            pass

        if check_recent_prisoners(proposed, recent):
            twitter.tweet(proposed)
            break

    return None


if __name__ == "__main__":
    main()
