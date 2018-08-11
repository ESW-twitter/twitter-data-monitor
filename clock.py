from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.scheduler import scheduler
from app.models import Actor
from app.capture_jobs import actors_job, relations_job, tweets_job
import time
import os

jobstores = {
    'default': SQLAlchemyJobStore(os.environ.get('DATABASE_URL'))
}

scheduler = BlockingScheduler(jobstores=jobstores)

scheduler.start()
 