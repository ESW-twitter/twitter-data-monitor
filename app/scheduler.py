from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.capture_jobs import actors_job, tweets_job, relations_job, reschedule_all_jobs
from app.models import Actor
import threading

scheduler = BackgroundScheduler()

#adding all actors job to the scheduler
scheduler.add_job(actors_job().start, 'interval', days=7, id='actors')

#adding relations job to the scheduler
scheduler.add_job(relations_job().start, 'interval', days=7, id='relations')

#adding tweets job for each actor
actors = Actor.query.all()
for actor in actors:
	id = actor.id
	scheduler.add_job(tweets_job(id=id).start, 'interval', days=7, id=id)
		
scheduler.start()

# avoiding a great number of threads starting at the same time
rescheduling = reschedule_all_jobs(scheduler)

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

def reschedule_job(id, minutes):
	if id=='actors' and minutes <2:
		print("ERRO! Intervalo mínimo é 2 minutos!")
		return 
	elif id=='relations' and minutes <10:
		print("ERRO! Intervalo mínimo é 10 minutos!")
		return
	elif minutes < 2:
		print("ERRO! Intervalo mínimo é 2 minutos!")	 
	
	try:
		scheduler.reschedule_job(job_id=id, trigger=IntervalTrigger(minutes=minutes))
		print("Intervalo de "+id+" modificado para "+str(minutes))
	except Exception as e:
		print(e)



