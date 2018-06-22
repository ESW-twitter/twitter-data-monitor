from modules.csv_builder import CsvBuilder, list_to_row
from modules.twitter_api import extract_retweeted_author_id
from modules.twitter_user import TwitterUser
import json
from app.models import Actor
from datetime import datetime, timedelta


def capture_actors():
	'''
	Performs a capture of quantitative information of all Actors returning a CSV 
	'''
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
	'''
	Performs a capture of all Tweets from the Actor specified by id from the date specified
	Returning a CSV
	'''
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
	'''
	Performs a capture of retweet relation between all Actors from the date specified
	Returning a CSV
	'''
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



def capture_relations_timeline(day=1, month=1, year=2018):
	'''
	Performs a capture of retweet relation between all Actors from the date specified and separeted by week
	Returning a CSV
	'''
	header_json = json.load(open("helpers/relations_attributes.json"))
	header_json = header_json[:2]
	ids = []
	actors = Actor.query.all()

	date = datetime(day=day, month=month, year=year)
	date_list = []
	while date <= datetime.now():
		date_list.append(date)
		header_json.append({'attribute': str(date).split(" ")[0]})
		date = date + timedelta(weeks=1)
	date_list.append(datetime.now())	
	csv = CsvBuilder(header_json)

	for actor in actors:
		ids.append(actor.id)

	relations = {}	
		
	for actor in actors:
		print("Capturing RT-relations of", actor.name, "week by week")
		user = TwitterUser(actor.id)
		id_subset = [x for x in ids if x != actor.id]	
		if user.existence==True:
			tweets = user.retrieve_tweets_from(day=day, month=month, year=year, raw=True)
				
			mentions_ids = extract_retweeted_author_id(tweets)

			for mention in mentions_ids:
				if mention[0] in id_subset:
					retweeted = Actor.query.filter_by(id=str(mention[0])).first().username
					relations[actor.username+";"+retweeted] = {}

			by_week = split_tweets(tweets, date_list)	

			for week in by_week.keys():
				week_mentions = extract_retweeted_author_id(by_week[week])
				for mention in week_mentions:
					if mention[0] in id_subset:
						retweeted = Actor.query.filter_by(id=str(mention[0])).first().username
						relations[actor.username+";"+retweeted][week]=mention[1]
				
	for relation in relations.keys():
		row = relation
		for i in range(0,len(date_list)-1):
			if str(date_list[i].date()) in relations[relation].keys():
				row = row + ";" + str(relations[relation][str(date_list[i].date())])
			else:
				row = row + ";0"
		row = row + ";\n"
		csv.add_row(row) 


	return csv	



def split_tweets(tweets, date_list):
	'''
	returns a dictionary of tweets divided using the intervals in date_list.
	each key of the dicitionary is a date from the list, and the content comprises the tweets between that date and the
	next on the list. 
	obs: the last date on the list won't appear on the dictionary keys.  
	'''

	dic = {}
	for i in range(1,len(date_list)):
		dic[str(date_list[i-1]).split(" ")[0]]=[]
		for tweet in tweets:
			if tweet.created_at>=date_list[i-1] and tweet.created_at<date_list[i]:
				dic[str(date_list[i-1]).split(" ")[0]].append(tweet)
	return dic

