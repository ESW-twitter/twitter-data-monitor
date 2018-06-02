#coding: utf-8
from app import app, db
from app.models import TweetReport, Actor
from app.scheduler import scheduler, retrieve_interval, retrieve_next_runtime, reschedule_job
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger



@app.route('/tweets/mudarintervalo/<id>', methods=['POST'])
def tweet_change_interval(id):
    
    actor = Actor.query.filter_by(id=id).first()
    if not actor:
        return redirect('/')

    if request.method == 'POST':
        minutes = int(request.form['intervalo'])
        reschedule_job(id=actor.id, minutes=minutes)

    return redirect("/tweets/view/"+actor.username)


@app.route('/tweets/view/<username>')
def tweets(username):
    actor = Actor.query.filter_by(username=username).first()
    if not actor:
        return redirect('/')

    interval = retrieve_interval(actor.id)
    next_run = retrieve_next_runtime(actor.id)    

    reports = TweetReport.query.filter_by(actor_id=actor.id)

    return render_template('tweets.html', reports=reports, intervalo=interval, actor=actor, next=next_run)


@app.route('/tweets/delete/', methods=['POST'])
def tweet_delete():
    if request.method == 'POST':
        try:
            req_id = int(request.form['id'])
            report = TweetReport.query.filter_by(id= req_id).first()
            username = Actor.query.filter_by(id=req_id).first().username
            db.session.delete(report)
            db.session.commit()
            print("Apagada captura de ", report.date, report.hour)
            return redirect("/tweets/view/"+username)
        except Exception as e:
            print("Não foi possível apagar", e)
        
    return redirect("/")

@app.route('/tweets/download_csv/<rep_id>')
def tweet_download_csv(rep_id):
    

    report = TweetReport.query.filter_by(id=rep_id).first()
    
    actor = Actor.query.filter_by(id=report.actor_id).first()
    if not actor:
        return redirect('/')

    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format(actor.username+"-"+report.date+"_"+report.hour)
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response
