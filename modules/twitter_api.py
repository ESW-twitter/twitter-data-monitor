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

def extract_hashtags(tweet_list):
    '''
    returns a list of hashtags and occurrence contained in the tweet_list ordered by greater occurrence
    '''
    hashtags = []
    lower = []
    if type(tweet_list)==list:
        for tweet in tweet_list:
            for hashtag in tweet.entities['hashtags']:
                lower.append(hashtag['text'].lower())
                hashtags.append(hashtag['text'])

    else:
        tweet = tweet_list
        for hashtag in tweet.entities['hashtags']:
            lower.append(hashtag['text'].lower())
            hashtags.append(hashtag['text'])                    
                
    mapped = [[x,lower.count(x)] for x in set(lower)]
    mapped.sort(key=lambda tuple: tuple[1], reverse=True)

    for item in mapped:
        item[0] = hashtags[lower.index(item[0])] 

    final = [x[0] for x in mapped]

    return final


def extract_mentions(tweet_list):
    '''
    returns a list of mentions and occurrence contained in the tweet_list ordered by greater occurrence
    '''
    mentions = []
    if type(tweet_list)==list:
        for tweet in tweet_list:
            for mention in tweet.entities['user_mentions']:
                mentions.append(mention['screen_name'])
    else:
        tweet = tweet_list
        for mention in tweet.entities['user_mentions']:
            mentions.append(mention['screen_name'])            

    mapped = [[x,mentions.count(x)] for x in set(mentions)]
    mapped.sort(key=lambda tuple: tuple[1], reverse=True)
    final = [x[0] for x in mapped]
    return final

def extract_retweets(tweet_list):
    retweets = 0
    if type(tweet_list)==list:
        for tweet in tweet_list:
            retweets += tweet.retweet_count
    else:
        tweet = tweet_list
        retweets += tweet.retweet_count

    return retweets

def extract_author(tweet):
    if hasattr(tweet, 'retweeted_status'):
        return tweet.retweeted_status.author.screen_name
    else:
        return ""
            
def extract_favorites(tweet_list):
    favorites = 0
    if type(tweet_list)==list:
        for tweet in tweet_list:
            favorites += tweet.favorite_count
    else:
        tweet = tweet_list
        favorites += tweet.favorite_count
                
    return favorites

def extract_retweeted_author_id(tweet_list):
    ids = []
    if type(tweet_list)==list:
        for tweet in tweet_list:
            if hasattr(tweet, 'retweeted_status'):
                ids.append(tweet.retweeted_status.author.id_str)
    else:
        tweet = tweet_list
        if hasattr(tweet, 'retweeted_status'):
            ids.append(tweet.retweeted_status.author.id_str)

    mapped = [[x,ids.count(x)] for x in set(ids)]
    mapped.sort(key=lambda tuple: tuple[1], reverse=True)        

    return mapped    
