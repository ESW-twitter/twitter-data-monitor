import csv
import datetime
import os
import json
import tweepy
from dateutil.relativedelta import relativedelta

class TwitterAPI(tweepy.API):
    def __init__(self):
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        tweepy.API.__init__(self,auth)

    def get_user_tweets_from(self,username, day, month, year):
        tweet_list = []
        min_date = datetime.datetime(year, month, day)
        temp = self.user_timeline(screen_name=username, count=200, tweet_mode='extended')
        while True:
            if not len(temp) > 0:
                break
            if not temp[-1].created_at >= min_date:
                break
            tweet_list.extend(temp)
            temp = self.user_timeline(screen_name=username, max_id=(temp[-1].id -1), count=200, tweet_mode='extended')


        for tweet in temp:
            if tweet.created_at >= min_date:
                tweet_list.append(tweet)

        return tweet_list

    @staticmethod
    def extract_hashtags(tweet_list):
        hashtags = []
        for tweet in tweet_list:
            for hashtag in tweet.entities['hashtags']:
                hashtags.append(hashtag['text'])
        return list(set(hashtags))
