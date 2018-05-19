from app import app
import json
from flask import jsonify
from modules.twitter_user import TwitterUser


@app.route('/api/actors')
def api_get_actors():
	data = {}
	politicians = []
	actors_count = 0
	actors = json.load(open("helpers/politicians.json"))
	for actor in actors:
		if actor['twitter_handle'] != "":
			actors_count += 1
			politicians.append(actor['twitter_handle'])
	data['code'] = '200'
	data['message'] = 'Success'
	data['length'] = actors_count
	data['actors'] = politicians

	return jsonify(data)
# 
# @app.route('/api/actors/datetimes')
# def api_get_actors():
# 	data = {}



@app.route('/api/actor/<username>/', defaults={ 'date': None })
@app.route('/api/actor/<username>/<date>')
def api_get_actor_account_date(username,date):
	## If not specified date, API will return current values from Tweepy API.
	if date == None :
		user = TwitterUser(username)
		if user.existence == False :
			data = {'code': '400', 'message': 'Bad Request', 'details': 'Invalid username.'}
			return jsonify(data)
		else:
			data = {'code': '200', 'message':'Success', 'id': user.id, 'username': user.username, 'name': user.name, 'followers_count': user.followers_count, 'tweets_count': user.tweets_count, 'following_count': user.following_count, 'likes_count': user.likes_count }
			return jsonify(data)


#
# @app.route('/api/tweets/<username>/', defaults={'count': 20, 'since': None, 'until': None})
# @app.route('/api/actor/<username>/<count>/<since>/<until>')
# def api_get_actor_tweets_count_since_until(username, count, since, until):
# 	pass
#

	## basic information, tweets, array de datas de basic information, array de datas de tweets
