from modules.twitter_api import TwitterAPI, extract_favorites,extract_hashtags,extract_mentions,extract_retweets, extract_author
from modules.csv_builder import list_to_string

class TwitterUser:

	def __init__(self,username):
		api = TwitterAPI()
		if username != '':
			try:
				user = api.get_user(username)
				self.existence = True
				self.id = user.id
				self.username = user.screen_name
				self.name = user.name
				self.followers_count = user.followers_count
				self.tweets_count = user.statuses_count
				self.following_count = user.friends_count
				self.likes_count = user.favourites_count
			except Exception as e:
				self.existence = False
		else:
			self.existence = False


	def retrieve_tweets_from(self, day, month, year, hour=0, minute=0):
		api = TwitterAPI()
		tweets_raw = api.get_user_tweets_from(self.username, day, month, year, hour, minute)
		tweet_list = []

		for tweet_raw in tweets_raw:
			tweet = []
			tweet.append(str(tweet_raw.created_at))	
			tweet.append(tweet_raw.full_text.replace('\n',' ').replace(';', ' ').replace('"', "'"))
			tweet.append(extract_author(tweet_raw))
			tweet.append(extract_retweets(tweet_raw))
			tweet.append(extract_favorites(tweet_raw))
			tweet.append(list_to_string(extract_hashtags(tweet_raw), hashtag=True))
			tweet.append(list_to_string(extract_mentions(tweet_raw)))
			tweet_list.append(tweet)

		return tweet_list	