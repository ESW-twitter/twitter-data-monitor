from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.capture_jobs import actors_job, tweets_job, reschedule_tweet_jobs
import threading
import json
import time
from app.models import Actor

scheduler = BackgroundScheduler()

#adding all actors job to the scheduler
scheduler.add_job(actors_job().start, 'interval', days=7, id='actors')

actors = Actor.query.all()
for actor in actors:
	username = actor.username
	if len(username) > 2:
		scheduler.add_job(tweets_job(username=username).start, 'interval', days=7, id=username)
		
scheduler.start()

# avoiding a great number of threads starting at the same time
rescheduling = reschedule_tweet_jobs(scheduler)
rescheduling.start()

def retrieve_interval(id):
	try:
		job = scheduler.get_job(id)
		interval = int(job.trigger.interval_length/60)
	except Exception as e:
		interval = "unknown"
	return interval    


def retrieve_next_runtime(id):	
	try:
		job = scheduler.get_job(id)
		next_run = str(job.next_run_time).split(".")[0] 
	except Exception as e:
		next_run = "unknown"
	return next_run    

def reschedule_tweet_job(id, minutes):
	try:
		if minutes >=2:
			scheduler.reschedule_job(job_id=id, trigger=IntervalTrigger(minutes=minutes))
			print("Intervalo de "+id+" modificado para "+str(minutes))
		else:
			print("ERRO! Intervalo mínimo é de 2 minutos!")    
	except Exception as e:
		print(e)
		print("ERRO! Não foi possível mudar o intervalo.")

def reschedule_actors_job(minutes):
	try:
		if minutes >=2:
			scheduler.reschedule_job('actors', trigger=IntervalTrigger(minutes=minutes))
			print("Intervalo de captura de todos os atores modificado para "+str(minutes))
		else:
			print("ERRO! Intervalo mínimo é de 2 minutos!")    
	except Exception as e:
		print(e)
		print("ERRO! Não foi possível mudar o intervalo.")

def reschedule_all_tweet_jobs(minutes):
	try:
		if minutes>=2:
			rescheduling = reschedule_tweet_jobs(scheduler, minutes=minutes)
			rescheduling.start()
		else:
			print("ERRO! Intervalo mínimo é de 2 minutos!")
	except Exception as e:
		print(e)
		print("Erro não foi possível mudar o intervalo de todas capturas de Tweets!")
	


