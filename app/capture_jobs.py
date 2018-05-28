from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger
import threading
from modules.twitter_user import TwitterUser
from modules.capture import capture_actors, capture_tweets, capture_relations
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from app import db 
from app.models import ActorReport, TweetReport, RelationReport, Actor
import json
import time

class actors_job:
    def __init__(self):
        pass

    def isAlive(self):
        try:
            return self.thread.isAlive()    
        except:
            return False    

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
        self.id = id

    def isAlive(self):
        try:
            return self.thread.isAlive()    
        except:
            return False

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        csv = capture_tweets(self.id)
        date = str(datetime.utcnow()).split(" ")[0]        
        hour = str(datetime.utcnow()).split(" ")[1].split(".")[0]

        if csv == "none":
            return

        f = TweetReport(date = date, hour= hour, actor_id = self.id, csv_content=csv.content.encode())
        db.session.add(f)
        db.session.commit()

class relations_job:
    def __init__(self):
        pass

    def isAlive(self):
        try:
            return self.thread.isAlive()    
        except:
            return False

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       
        self.thread.start()

    def run(self):
        check_actors_usernames()
        csv = capture_relations()
        date = str(datetime.utcnow()).split(" ")[0]        
        hour = str(datetime.utcnow()).split(" ")[1].split(".")[0]        
        
        f = RelationReport(date= date, hour=hour, csv_content= csv.content.encode())
        db.session.add(f)
        db.session.commit()
    

class reschedule_all_jobs:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        jobs = self.scheduler.get_jobs()
        for job in jobs:
            time.sleep(60)
            job.reschedule(trigger=IntervalTrigger(seconds=job.trigger.interval_length)) 


def check_actors_usernames():
    print("Checking if actors usernames remain the same...")
    actors = Actor.query.all()
    for actor in actors:
        user = TwitterUser(actor.id)
        if user.existence == True:  
            if user.username != actor.username:
                print(actor.username,"changed to:", user.username)
                Actor.query.filter_by(id=actor.id).update(dict(username=user.username))
                db.session.commit()


def capture_tweets_from_all():
    actors = Actor.query.all()
    for actor in actors:        
        id = actor.id
        job = tweets_job(id)
        job.start()
        time.sleep(15)    
