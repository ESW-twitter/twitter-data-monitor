#coding: utf-8
from app import app, db
from app.models import ActorReport
from app.scheduler import scheduler
from flask import Flask, make_response, request, render_template, redirect
from apscheduler.triggers.interval import IntervalTrigger



@app.route('/atores/mudarintervalo', methods=['POST'])
def change_interval():
    if request.method == 'POST':
        try:
            req_interval = int(request.form['intervalo'])
            if req_interval >=1:
                scheduler.reschedule_job('actors', trigger=IntervalTrigger(minutes=req_interval))
                print("Intervalo de captura geral modificado para "+str(req_interval))
            else:
                print("ERRO! Intervalo máximo é 5 minutos!")    
        except Exception as e:
            print("ERRO! Não foi possível mudar o intervalo.")

    return redirect("/atores/")


@app.route('/atores/')
def actors():
    try:
        job = scheduler.get_job('actors')
        interval = int(job.trigger.interval_length/60)
        next_run = str(job.next_run_time).split(".")[0] 
    except Exception as e:
        interval = "unknown"
        next_run = "unknown"
    
    reports = ActorReport.query.all()
    for report in reports:
        report.date = report.date.split(".")[0]

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
    cd = 'attachment; filename={}.csv'.format(report.date.split(".")[0])
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response
