from app import app
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger
from app.models import Actor

@app.route('/')
def main_page():
	names = []
	actors = Actor.query.all()
	names.sort(key=lambda x: x.name)

	return render_template('main.html', actors=actors )
	