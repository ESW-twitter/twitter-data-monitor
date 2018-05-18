from modules.csv_builder import CsvBuilder, list_to_row
from modules.twitter_user import TwitterUser
import json

def capture_actors():
	actors = json.load(open("helpers/politicians.json"))
	header_json = json.load(open("helpers/actors_attributes.json"))
	csv = CsvBuilder(header_json)
	print("Capturing Actors information")

	for row in actors:
		user = TwitterUser(row["twitter_handle"])
		
		if user.existence == True:
			print("Retrieving information from ", user.username)
			row = list_to_row([user.name, user.username, user.followers_count, user.following_count, user.likes_count, user.tweets_count])
			csv.add_row(row)
			

	return csv


def capture_tweets(username, day=1, month=1, year=2018):
	header_json = json.load(open("helpers/tweets_attributes.json"))

	csv = CsvBuilder(header_json)

	user = TwitterUser(username)
	if user.existence == True:
		print("Capturing "+username+" tweets")
		tweets = user.retrieve_tweets_from(day,month,year)
		for tweet in tweets:
			row = list_to_row(tweet)
			csv.add_row(row)	

	else: 
		csv = "none"

	return csv	