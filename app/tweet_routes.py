#coding: utf-8
from app import app, db
from app.models import TweetReport, Actor
from app.scheduler import scheduler, retrieve_interval, retrieve_next_runtime, reschedule_tweet_job
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger



@app.route('/tweets/mudarintervalo/<username>', methods=['POST'])
def tweet_change_interval(username):
    if request.method == 'POST':
        minutes = int(request.form['intervalo'])
        reschedule_tweet_job(username, minutes)

    return redirect("/tweets/view/"+username)


@app.route('/tweets/view/<username>')
def tweets(username):
    
    interval = retrieve_interval(username)
    next_run = retrieve_next_runtime(username) 

    actor = Actor.query.filter_by(username=username).first()
    if not actor:
        return redirect('/')

    reports = TweetReport.query.filter_by(username=username)
    
    return render_template('tweets.html', reports=reports, intervalo=interval, actor=actor, next=next_run)


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
