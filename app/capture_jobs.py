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
    def __init__(self):
        self.thread = threading.Thread(target=self.run, args=())

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        check_actors_usernames()
        csv = capture_actors()
        date = str(datetime.utcnow()).split(" ")[0]        
        hour = str(datetime.utcnow()).split(" ")[1].split(".")[0]        
        
        f = ActorReport(date= date, hour=hour, csv_content= csv.content.encode())
        db.session.add(f)
        db.session.commit()
          

class tweets_job:
    def __init__(self, id):
        self.thread = threading.Thread(target=self.run, args=())
        self.id = id

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        actors = Actor.query.all()
        for actor in actors:
            user = TwitterUser(actor.id)
            if user.username != actor.username:
                Actor.query.filter_by(id=actor.id).update(dict(username=user.username))
                db.session.commit()

        csv = capture_tweets(self.id)
        date = str(datetime.utcnow()).split(" ")[0]        
        hour = str(datetime.utcnow()).split(" ")[1].split(".")[0]

        if csv == "none":
            return

        f = TweetReport(date = date, hour= hour, actor_id = self.id, csv_content=csv.content.encode())
        db.session.add(f)
        db.session.commit()
    

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
            time.sleep(20)
            id = actor.id
            job = self.scheduler.get_job(id)
            job.reschedule(trigger=IntervalTrigger(minutes=self.minutes))

def check_actors_usernames():
    actors = Actor.query.all()
    for actor in actors:
        user = TwitterUser(actor.id)
        if user.existence == True:  
            if user.username != actor.username:
                Actor.query.filter_by(id=actor.id).update(dict(username=user.username))
                db.session.commit()


def capture_tweets_from_all():
    actors = Actor.query.all()
    for actor in actors:        
        id = actor.id
        job = tweets_job(id)
        job.start()
        time.sleep(5)    
