from modules.csv_builder import CsvBuilder, list_to_row
from modules.twitter_user import TwitterUser
import json
from app.models import Actor

def capture_actors():
	actors = Actor.query.all()
	header_json = json.load(open("helpers/actors_attributes.json"))
	csv = CsvBuilder(header_json)
	print("Capturing Actors information")

	for actor in actors:
		user = TwitterUser(actor.id)
		
		if user.existence == True:
			print("Retrieving information from ", user.username)
			row = list_to_row([actor.id, user.name, user.username, user.followers_count, user.following_count, user.likes_count, user.tweets_count])
			csv.add_row(row)
			

	return csv


def capture_tweets(id, day=1, month=1, year=2018):
	header_json = json.load(open("helpers/tweets_attributes.json"))

	csv = CsvBuilder(header_json)

	user = TwitterUser(id)
	if user.existence == True:
		print("Capturing "+user.name+" tweets")
		tweets = user.retrieve_tweets_from(day,month,year)
		for tweet in tweets:
			row = list_to_row(tweet)
			csv.add_row(row)	

	else: 
		csv = "none"

	return csv	