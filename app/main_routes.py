from app import app, db
from app.scheduler import scheduler
from app.capture_jobs import tweets_job
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger
from app.models import Actor
from unidecode import unidecode
from modules.twitter_user import TwitterUser

@app.route('/')
def main_page():
	names = []
	actors = Actor.query.all()
	names.sort(key=lambda x: x.name)

	return render_template('main.html', actors=actors )



@app.route('/addactor', methods=['POST'])
def add_actor():
	if request.method == 'POST':
		try:
			username = request.form['username']
			user = TwitterUser(username)
			if user.existence == True:
				name = user.name
				name = unidecode(name)
				f = Actor(id = int(user.id), username=username, name= name)
				db.session.add(f)
				db.session.commit()
				scheduler.add_job(tweets_job(id=user.id).start, 'interval', days=7, id=user.id)
				print("Ator", username,"adicionado")
			else:
				print("Usuario",username,"não existe!")	
		except:
			pass		

	return redirect("/")

@app.route('/removeactor', methods=['POST'])
def remove_actor():
	if request.method == 'POST':
		try:

			actor_id = request.form['actor']
			print("deletando", actor_id)
			user = Actor.query.filter_by(id=actor_id).first()
			db.session.delete(user)
			db.session.commit()
			scheduler.remove_job(job_id=actor_id)

			#falta remover todos os CSV's do ator
		except:
			pass	
			
	return redirect("/")
