from datetime import datetime, timedelta
import threading
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    csv_content = db.Column(db.LargeBinary)

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content

    def __repr__(self):
        return '<Report %r>' % self.id


def get_last_capture():
    reports = Report.query.all()
    reports.sort(key=lambda x: x.id, reverse=True)
    last_capture = reports[0].date.split(" ")[0].split("-")
    day = int(last_capture[2])
    month = int(last_capture[1])
    year = int(last_capture[0])
    day_hour = reports[0].date.split(" ")[1].split(":")
    hour = int(day_hour[0])
    minute= int(day_hour[1])
    return datetime(year, month, day, hour, minute, 0)


class csv_report:
  
    def __init__(self):
        self.thread = threading.Thread(target=self.run, args=())

    def start(self):    
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                       # Daemonize thread
        self.thread.start()

    def run(self):
        csv_content = "nome;seguidores;tweets;seguindo;curtidas;retweets;favorites;hashtags;mentions\n"
        file = open("helpers/politicians.json")
        actors = json.load(file)

        try:
            last_capture = get_last_capture()
            day = int(last_capture.day)
            month = int(last_capture.month)
            year = int(last_capture.year)
            hour = int(last_capture.hour)
            minute= int(last_capture.minute)
        except Exception as e:
                yesterday = datetime.utcnow() - timedelta(days=1)
                day = yesterday.day
                month = yesterday.month
                year = yesterday.year
                hour = 0
                minute = 0
        
        print("Collecting information from "+str(year)+"/"+str(month)+"/"+str(day)+" "+str(hour)+":"+str(minute)+" to date")
          
        for row in actors:
            user = TwitterUser(row["twitter_handle"])
            if user.existence == True:
                print("Retrieving information of "+ str(user.username))
                user.retrieve_info_from(day, month, year, hour, minute)
                aux = "{};{};{};{};{};{};{};{};{};\n".format(user.name, user.followers_count,
                user.tweets_count, user.following_count, user.likes_count, user.retweets_count, user.favorites_count, CsvBuilder.list_to_string(user.hashtags, hashtag=True),CsvBuilder.list_to_string(user.mentions))
                csv_content = csv_content + aux        
                
        name = str(datetime.utcnow()).split(".")[0]#+"-from-"+str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)        
        f = Report(name, csv_content.encode())

        if get_last_capture() < datetime.utcnow() - timedelta(minutes=1):
            db.session.add(f)
            db.session.commit()
        else:
            print("ERRO: Não salvo no BD! Só é permitida uma captura por minuto")

       

