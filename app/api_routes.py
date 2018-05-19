from app import app
import json
from flask import jsonify

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
	data['length'] = actors_count
	data['actors'] = politicians

	return jsonify(data)


## { actors: [ { 'handle': 'handle1'} , { 'handle2': 'handle' }]}
