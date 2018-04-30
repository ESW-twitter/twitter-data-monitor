import csv
import datetime
import os
import json
import tweepy
from dateutil.relativedelta import relativedelta

class TwitterAPI(tweepy.API):

    def __init__(self,keys="../helpers/keys.json"):
        filepath = os.path.join(os.path.dirname(__file__), keys)
        file = open(filepath)
        keys = json.load(file)
        consumer_key=keys[0]['consumer_key']
        consumer_secret=keys[0]['consumer_secret']
        access_token=keys[0]['access_token']
        access_token_secret=keys[0]['access_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        tweepy.API.__init__(self,auth)
        file.close()

    def get_user_tweets_from(self,username, day, month, year, hour=0, minute=0):
        tweet_list = []
        min_date = datetime.datetime(year, month, day, hour, minute, 0)
        kwargs = {'screen_name': username,'count': 200,'tweet_mode': 'extended'}
        
        while True:
            temp = self.user_timeline(**kwargs) 
            if not temp or temp[-1].created_at < min_date:
                break
            tweet_list.extend(temp)    
            max_id = temp[-1].id - 1
            kwargs.update({'max_id': max_id})    

        temp = [i for i in temp if i.created_at >= min_date]
        tweet_list.extend(temp)  
        return tweet_list


    @staticmethod
    def extract_hashtags(tweet_list):
        '''
        returns a list of hashtags contained in the tweet_list ordered by greater occurrence
        '''
        hashtags = []
        lower = []
        for tweet in tweet_list:
            for hashtag in tweet.entities['hashtags']:
                lower.append(hashtag['text'].lower())
                hashtags.append(hashtag['text'])
        
        mapped = [[x,lower.count(x)] for x in set(lower)]        
        mapped.sort(key=lambda tuple: tuple[1], reverse=True)
        final = [x[0] for x in mapped] 

        for hashtag in hashtags:
            if hashtag.lower() in final:
                final[final.index(hashtag.lower())] = hashtag

        return final
    

    @staticmethod
    def extract_mentions(tweet_list):
        '''
        returns a list of mentions contained in the tweet_list ordered by greater occurrence
        '''
        mentions = []
        for tweet in tweet_list:
            for mention in tweet.entities['user_mentions']:
                mentions.append(mention['screen_name'])    

        mapped = [[x,mentions.count(x)] for x in set(mentions)]
        mapped.sort(key=lambda tuple: tuple[1], reverse=True)

        return [x[0] for x in mapped] 









