import csv
import os
import json
from datetime import datetime, timedelta
import threading
from flask import Flask, make_response, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
os.environ["TwITTER_CAPTURING"] = "False"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60))
    csv_content = db.Column(db.LargeBinary)

    def __init__(self, date, csv_content):
        self.date = date
        self.csv_content = csv_content

    def __repr__(self):
        return '<Report %r>' % self.id


class generate_csv_report:

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                       # Daemonize thread
        thread.start()                   
    def run(self):
        os.environ["TwITTER_CAPTURING"] = "True"
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
            day_hour = reports[0].date.split(" ")[1].split(":")
            hour = int(day_hour[0])
            minute= int(day_hour[1])
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



        name = str(datetime.utcnow())#+"-from-"+str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)        
        f = Report(name, csv_content.encode())
        db.session.add(f)
        db.session.commit()
        os.environ["TwITTER_CAPTURING"] = "False"
        
@app.route('/')
def hello_world():
    reports = Report.query.all()
    for report in reports:
        report.date = report.date.split(".")[0]
    return render_template('main.html', reports=reports)


@app.route('/performcapture')
def perform():
    if os.environ.get("TwITTER_CAPTURING") == "False":
        capture = generate_csv_report()
    else:
        print("CAPTURA JA ESTA SENDO FEITA")
    return redirect("/")


@app.route('/download_csv/<rid>')
def download_csv(rid):
    report = Report.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format(report.date.split(".")[0])
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response

if __name__ == '__main__':
    app.run(threaded=True)
    


