import pytest
import warnings
import datetime
import modules
import pickle
from modules.twitter_api import TwitterAPI
from dateutil.relativedelta import relativedelta

class TestTwitterAPI():
# time consuming
    def test_time_range(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        api = TwitterAPI()
        tweets2 = api.get_user_tweets_from('cirogomes', day=2, month=4, year=2018)
        assert(tweets2[-1].created_at >= datetime.datetime(2018, 4, 2)) == True


    def test_hashtags(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
        hashtags = TwitterAPI.extract_hashtags(tweets)
        assert 'MaioMesDaCiencia' in hashtags
        assert 'ResolviEsperar' in hashtags
        assert 'Codaí' in hashtags

    def test_mentions(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
        mentions = TwitterAPI.extract_mentions(tweets)
        assert 'davirsimoes' in mentions
        assert 'sonolencio' in mentions
        assert 'Pirulla25' in mentions

    def test_retweets(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
        assert 592 == TwitterAPI.extract_retweets(tweets)

    def test_favorites(self):
        warnings.filterwarnings("ignore", category=ResourceWarning)
        tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
        assert 5718 == TwitterAPI.extract_favorites(tweets)

