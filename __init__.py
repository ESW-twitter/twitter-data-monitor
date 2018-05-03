import csv
import os
import json
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modules.twitter_user import TwitterUser
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:password@localhost/twitter_db"
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    csv_content = db.Column(db.LargeBinary)

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content

    def __repr__(self):
        return '<Report %r>' % self.id

def generate_csv_report():
    csv_content = "nome;seguidores;tweets;seguindo;curtidas;hashtags;\n"
    file = open("helpers/politicians.json")
    actors = json.load(file)
    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            aux = "{};{};{};{};{};\n".format(user.name, user.followers_count, user.tweets_count, user.following_count, user.likes_count)
            csv_content = csv_content + aux

    f = Report(datetime.datetime.now().strftime('%d/%m/%Y'), csv_content.encode())
    db.session.add(f)
    db.session.commit()

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=2)
def generate_reports():
    print('oi')
    generate_csv_report()


@app.route('/')
def hello_world():
   return  'Hello World'

if __name__ == '__main__':
    app.run()
