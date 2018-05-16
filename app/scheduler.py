from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.capture_jobs import actors_job, tweets_job
import threading
import json
import time


scheduler = BackgroundScheduler()

#adding all actors job to the scheduler
scheduler.add_job(actors_job().start, 'interval', days=7, id='actors')
actors = json.load(open("helpers/politicians.json"))
for row in actors:
	username = row["twitter_handle"]
	if len(username) > 2:
		scheduler.add_job(tweets_job(username=username).start, 'interval', days=7, id=username)
		
scheduler.start()


class bootstrap_jobs:
    def __init__(self):
        self.thread = threading.Thread(target=self.run, args=())

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        actors = json.load(open("helpers/politicians.json"))
        for row in actors:
            time.sleep(20)
            username = row["twitter_handle"]
            if len(username) > 2:
                job = scheduler.get_job(username)
                job.reschedule(trigger=IntervalTrigger(days=7))

reschedule_jobs = bootstrap_jobs()
reschedule_jobs.start()
