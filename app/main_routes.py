from app import app
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger
import json

@app.route('/')
def main_page():
	usernames = []
	actors = json.load(open("helpers/politicians.json"))
	for row in actors:
		username = row["twitter_handle"]
		if len(username) > 2:
			usernames.append(username)
	usernames.sort()

	return render_template('main.html', usernames=usernames)
