import csv
import os
import json
import datetime

from flask import Flask, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
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
    csv_content = "nome;seguidores;tweets;seguindo;curtidas;retweets;favorites;hashtags;mentions\n"
    file = open("helpers/politicians.json")
    actors = json.load(file)

    try:
        reports = Report.query.all()
        reports.sort(key=lambda x: x.id, reverse=True)
        last_capture = reports[0].date.split(" ")[0].split("-")
        day = int(last_capture[2])
        month = int(last_capture[1])
        year = int(last_capture[0])
        day_hour = reports[0].split(" ")[1].split(":")
        hour = int(day_hour[0])
        minute= int(day_hour[1])
    except Exception as e:
            yesterday = datetime.utcnow() - timedelta(days=1)
            day = yesterday.day
            month = yesterday.month
            year = yesterday.year
            hour = 0
            minute = 0

    for row in actors:
        user = TwitterUser(row["twitter_handle"])
        if user.existence == True:
            user.retrieve_info_from(day, month, year, hour, minute)
            aux = "{};{};{};{};{};{};{};{};{};\n".format(user.name, user.followers_count,
            user.tweets_count, user.following_count, user.likes_count, user.retweets_count, user.favorites_count, CsvBuilder.list_to_string(user.hashtags, hashtag=True),CsvBuilder.list_to_string(user.mentions))
            csv_content = csv_content + aux


    name = str(datetime.utcnow())+"-from-"+str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)        
    f = Report(name, csv_content.encode())
    db.session.add(f)
    db.session.commit()


@app.route('/')
def hello_world():
    reports = Report.query.all()
    return render_template('main.html', reports=reports)

@app.route('/download_csv/<rid>')
def download_csv(rid):
    report = Report.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format(report.date)
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response

if __name__ == '__main__':
    app.run()
