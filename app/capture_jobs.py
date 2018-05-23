from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger
import threading
from modules.twitter_user import TwitterUser
from modules.capture import capture_actors, capture_tweets
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from app import db 
from app.models import ActorReport, TweetReport, RelationReport, Actor
import json
import time

class actors_job:
    def __init__(self, in_local_File=False):
        self.thread = threading.Thread(target=self.run, args=())
        self.inFile=in_local_File

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        csv = capture_actors()
        date = str(datetime.utcnow()).split(".")[0]        
        
        if not self.inFile:
            f = ActorReport(date, csv.content.encode())
            db.session.add(f)
            db.session.commit()
        else:
            csv.save(name=date)    

class tweets_job:
    def __init__(self, username, in_local_File=False):
        self.thread = threading.Thread(target=self.run, args=())
        self.inFile=in_local_File
        self.username = username

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):

        csv = capture_tweets(self.username)
        date = str(datetime.utcnow()).split(".")[0]        
        
        if csv == "none":
            return

        if not self.inFile:
            f = TweetReport(date, self.username, csv.content.encode())
            db.session.add(f)
            db.session.commit()
        else:
            csv.save(name=date, dir=self.username)

class reschedule_tweet_jobs:
    def __init__(self, scheduler, minutes=10080):
        self.thread = threading.Thread(target=self.run, args=())
        self.scheduler = scheduler
        self.minutes = minutes
    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        actors = Actor.query.all()
        for actor in actors:
            time.sleep(20) #20 segundos entre um e outro
            username = actor.username
            if len(username) > 2:
                job = self.scheduler.get_job(username)
                job.reschedule(trigger=IntervalTrigger(self.minutes))


def capture_tweets_from_all():
    actors = Actor.query.all()
    for actor in actors:        
        username = actor.username
        job = tweets_job(username)
        job.start()
        time.sleep(5)    
