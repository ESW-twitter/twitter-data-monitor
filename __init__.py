import csv
import os
import json
import datetime

from flask import Flask, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy
from modules.twitter_user import TwitterUser
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
