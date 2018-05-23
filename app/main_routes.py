from app import app
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger
from app.models import Actor
from app.scheduler import retrieve_interval, reschedule_all_tweet_jobs

@app.route('/')
def main_page():
	names = []
	actors = Actor.query.all()
	names.sort(key=lambda x: x.name)

	return render_template('main.html', actors=actors)


@app.route('/mudarintervalotodostweets', methods=['POST'])
def all_tweets_change_interval():
	if request.method == 'POST':
		minutes = int(request.form['intervalo'])

	reschedule_all_tweet_jobs(minutes)		
	return redirect("/")
	