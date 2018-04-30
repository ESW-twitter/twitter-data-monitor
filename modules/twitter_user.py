from .twitter_api import TwitterAPI

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

	def retrieve_info_from(self, day, month, year, hour=0, minute=0):
		api = TwitterAPI()
		tweets = api.get_user_tweets_from(self.username, day, month, year, hour, minute)
		self.hashtags = TwitterAPI.extract_hashtags(tweets)
		self.mentions = TwitterAPI.extract_mentions(tweets)
		
	