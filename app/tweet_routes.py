#coding: utf-8
from app import app, db
from app.models import TweetReport
from app.scheduler import scheduler
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger
import json


@app.route('/tweets/mudarintervalo/<username>', methods=['POST'])
def tweet_change_interval(username):
    if request.method == 'POST':
        try:
            req_interval = int(request.form['intervalo'])
            if req_interval >=1:
                scheduler.reschedule_job(username, trigger=IntervalTrigger(minutes=req_interval))
                print("Intervalo de "+username+" modificado para "+str(req_interval))
            else:
                print("ERRO! Intervalo máximo é 5 minutos!")    
        except Exception as e:
            print("ERRO! Não foi possível mudar o intervalo.")

    return redirect("/tweets/view/"+username)


@app.route('/tweets/view/<username>')
def tweets(username):
    try:
        job = scheduler.get_job(username)
        if hasattr(job, 'trigger'):
            interval = int(job.trigger.interval_length/60)
            next_run = str(job.next_run_time).split(".")[0]
    except Exception as e:
        print(e)
        interval = "unknown"
        next_run = "unknown"


    usernames = []
    actors = json.load(open("helpers/politicians.json"))
    for row in actors:
        user = row["twitter_handle"]
        if len(username) > 2:
            usernames.append(user)    
    if username not in usernames:
        return redirect("/")       

    reports = TweetReport.query.filter_by(username=username)
    
    for report in reports:
        report.date = report.date.split(".")[0]

    return render_template('tweets.html', reports=reports, intervalo=interval, username=username, next=next_run)


@app.route('/tweets/delete/', methods=['POST'])
def tweet_delete():
    if request.method == 'POST':
        try:
            report_id = int(request.form['id'])
            report = TweetReport.query.filter_by(id= report_id).first()
            username = report.username
            db.session.delete(report)
            db.session.commit()
            print("Apagada captura de ", report.date)
            return redirect("/tweets/view/"+username)
        except Exception as e:
            print("Não foi possível apagar", e)
        
    return redirect("/")

@app.route('/tweets/download_csv/<rid>')
def tweet_download_csv(rid):
    report = TweetReport.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format(report.username+"-"+report.date.split(".")[0])
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response
