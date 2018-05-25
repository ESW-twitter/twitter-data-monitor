#coding: utf-8
from app import app, db
from app.models import ActorReport
from app.scheduler import scheduler, reschedule_actors_job, retrieve_interval, retrieve_next_runtime
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger



@app.route('/atores/mudarintervalo', methods=['POST'])
def change_interval():
    if request.method == 'POST':
        minutes = int(request.form['intervalo'])
        reschedule_actors_job(minutes)    

    return redirect("/atores/")


@app.route('/atores/')
def actors():
    
    interval = retrieve_interval('actors')
    next_run = retrieve_next_runtime('actors') 
    
    reports = ActorReport.query.all()

    return render_template('atores.html', reports=reports, intervalo=interval, next=next_run)

@app.route('/atores/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        try:
            report_id = int(request.form['id'])
            report = ActorReport.query.filter_by(id= report_id).first()
            db.session.delete(report)
            db.session.commit()
            print("Apagada captura de ", report.date)
        except Exception as e:
            print("Não foi possível apagar", e)
        
    return redirect("/atores/")

@app.route('/atores/download_csv/<rid>')
def download_csv(rid):
    report = ActorReport.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format(report.date+"_"+report.hour)
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response
