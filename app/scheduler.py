from apscheduler.schedulers.background import BackgroundScheduler
from app.capture_jobs import actors_job, tweets_job


scheduler = BackgroundScheduler()

#adding all actors job to the scheduler
actors_thread = actors_job()
scheduler.add_job(actors_thread.start, 'interval', minutes=1440, id='actors')

#adding test tweets job to the scheduler
#test_thread = tweets_job(username='jairbolsonaro', in_local_File=True)
#scheduler.add_job(test_thread.start, 'interval', minutes=1440, id='teste')

scheduler.start()