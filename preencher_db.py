from modules.twitter_user import TwitterUser
import os
import json
from unidecode import unidecode
from os.path import isfile, join

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class ActorReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, csv_content):
        self.date = date
        self.hour = hour
        self.csv_content = csv_content

    def __repr__(self):
        return '<ActorReport %r>' % self.id

class TweetReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    actor_id = db.Column(db.String(32))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, actor_id, csv_content):
        self.date = date
        self.csv_content = csv_content
        self.actor_id = actor_id
        self.hour = hour
    
    def __repr__(self):
        return '<TweetReport %r>' % self.id        

class RelationReport(db.Model):	
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    hour = db.Column(db.String(30))
    csv_content = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, date, hour, csv_content):
        self.date = date
        self.hour = hour
        self.csv_content = csv_content
    def __repr__(self):
        return '<RelationReport %r>' % self.id                

class Actor(db.Model): 
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(60))
    name = db.Column(db.String(60))

    def __init__(self, id,  username, name):
        self.id = id
        self.name = name
        self.username = username
    
    def __repr__(self):
        return '<Actor %r>' % self.username 



db.drop_all()
db.create_all()



# Adicionando atores do politicians.json
print("Adding Actors")
actors = json.load(open("helpers/politicians.json"))
for row in actors:
	username = row["twitter_handle"]
	user = TwitterUser(username)
	if user.existence == True:
		name = user.name
		name = unidecode(name)
		f = Actor(id = int(user.id), username=username, name= name)
		db.session.add(f)
		db.session.commit()
		print(name, "added")



# Adicinando CSV's de todos os atores presentes na pasta results
# print("Adding Actors CSV's")
# onlyfiles = [f for f in os.listdir(os.getcwd()+"/results/") if isfile(join(os.getcwd()+"/results/", f))]
# onlycsvs = [f for f in onlyfiles if f[-4:]=='.csv' and f != 'test.csv']
# onlycsvs.sort()
# for csv in onlycsvs:
# 	file = open('results/'+csv, 'r')
# 	csv_content = file.read().encode()
# 	date = csv[:-4].replace("_", ":")
# 	report = ActorReport(date, csv_content)
# 	db.session.add(report)
# 	db.session.commit()
# 	print(date, "capture added")


# Adicionando CSV's Tweets por ator contidos na pasta results/Tweet_Backup
# print("Adding Tweets from Actor CSV's")
# actors = Actor.query.all()
# for actor in actors:
# 	onlyfiles = [f for f in os.listdir(os.getcwd()+"/results/Tweet_Backup") if isfile(join(os.getcwd()+"/results/Tweet_Backup", f))]
# 	onlycsvs = [f for f in onlyfiles if f[-4:]=='.csv' and f != 'test.csv']
# 	onlyactorcsvs = [f for f in onlycsvs if f[:len(actor.username)]==actor.username]
# 	if len(onlyactorcsvs)==0:
# 		print(actor.nem, "não tem CSV", actor.username)

# 	for csv in onlyactorcsvs:
# 		file = open('results/Tweet_Backup/'+csv, 'r')
# 		csv_content = file.read().encode()
# 		date = csv[(len(actor.username)+1):-4].replace("_", ":")
# 		f = TweetReport(date=date, username=actor.username, csv_content=csv_content)
# 		db.session.add(f)
# 		db.session.commit()
# 		print(actor.username, "capture of", date, "added")









