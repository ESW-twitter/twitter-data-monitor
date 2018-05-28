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
	from app.scheduler import rescheduling
	can_resch_all = not rescheduling.thread.isAlive()

	return render_template('main.html', actors=actors, can_resc = can_resch_all )


@app.route('/mudarintervalotodostweets', methods=['POST'])
def all_tweets_change_interval():
	if request.method == 'POST':
		minutes = int(request.form['intervalo'])

	reschedule_all_tweet_jobs(minutes)
	return redirect("/")

@app.route('/addactor', methods=['POST'])
def add_actor():
	if request.method == 'POST':
		actor = request.form['add']

	return redirect("/")

@app.route('/removeactor', methods=['POST'])
def remove_actor():
	if request.method == 'POST':
		actor = request.form['remove']
		user = Actor.query.filter_by(username=actor)

	return redirect("/")
