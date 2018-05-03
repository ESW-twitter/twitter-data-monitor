import unittest
import warnings
import datetime
import modules
import pickle
from modules.twitter_api import TwitterAPI
from dateutil.relativedelta import relativedelta

class TestTwitterAPI(unittest.TestCase):

	def test_time_range(self):
		warnings.filterwarnings("ignore", category=ResourceWarning)
		api = TwitterAPI()
		tweets2 = api.get_user_tweets_from('cirogomes', day=2, month=4, year=2018)
		self.assertEqual(tweets2[-1].created_at >= datetime.datetime(2018, 4, 2), True)

	def test_hashtags(self):
		warnings.filterwarnings("ignore", category=ResourceWarning)
		tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
		hashtags = TwitterAPI.extract_hashtags(tweets)
		self.assertIn('MaioMesDaCiencia',hashtags)
		self.assertIn('ResolviEsperar',hashtags)
		self.assertIn('Codaí',hashtags)

	def test_mentions(self):
		warnings.filterwarnings("ignore", category=ResourceWarning)
		tweets = pickle.load(open('tests/tweetlist.p', 'rb'))
		mentions = TwitterAPI.extract_mentions(tweets)
		self.assertIn('davirsimoes', mentions)
		self.assertIn('sonolencio', mentions)
		self.assertIn('Pirulla25', mentions)	

if __name__ == '__main__':
    unittest.main()
