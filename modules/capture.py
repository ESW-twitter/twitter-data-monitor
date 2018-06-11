from modules.csv_builder import CsvBuilder, list_to_row
from modules.twitter_api import extract_retweeted_author_id
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

def capture_relations(day=1, month=1, year=2018):
	header_json = json.load(open("helpers/relations_attributes.json"))
	ids = []
	actors = Actor.query.all()

	csv = CsvBuilder(header_json)

	for actor in actors:
		ids.append(actor.id)

	for actor in actors:
		print("Capturing RT-relations of", actor.name)
		user = TwitterUser(actor.id)
		id_subset = [x for x in ids if x != actor.id]	
		if user.existence==True:
			tweets = user.retrieve_tweets_from(day=day, month=month, year=year, raw=True)
			mentions_ids = extract_retweeted_author_id(tweets)
			for mention in mentions_ids:
				if mention[0] in id_subset:
					retweeted = Actor.query.filter_by(id=str(mention[0])).first().username
					csv.add_row(actor.username+";"+retweeted+";"+str(mention[1])+"\n")


	return csv	





