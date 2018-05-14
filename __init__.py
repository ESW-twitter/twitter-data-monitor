import csv
import os
import json
from datetime import datetime, timedelta
import threading
from flask import Flask, make_response, request, render_template, redirect
from modules.twitter_user import TwitterUser
from modules.csv_builder import CsvBuilder
from apscheduler.schedulers.blocking import BlockingScheduler
from api import twitterAPI
from csv_report import csv_report, app, db, Report
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


api = twitterAPI(app)
capture = csv_report() 
os.environ['CAPTURE_INTERVAL']="1440"
interval = int(os.environ.get('CAPTURE_INTERVAL'))
scheduler = BackgroundScheduler()
scheduler.add_job(capture.start, 'interval', minutes=interval, id='capture')
scheduler.start()


@app.route('/mudarintervalo', methods=['POST'])
def change_interval():
    global interval
    if request.method == 'POST':
        try:
            req_interval = int(request.form['intervalo'])
            if req_interval >=5:
                os.environ['CAPTURE_INTERVAL']=str(req_interval)
                interval = req_interval
                scheduler.reschedule_job('capture', trigger=IntervalTrigger(minutes=interval))
                print("Intervalo modificado para "+str(interval))
            else:
                print("ERRO! Intervalo máximo é 5 minutos!")    
        except Exception as e:
            print("ERRO! Não foi possível mudar o intervalo.")

    return redirect("/")
        
@app.route('/')
def hello_world():
    
    reports = Report.query.all()
    for report in reports:
        report.date = report.date.split(".")[0]
    return render_template('main.html', reports=reports, intervalo=int(os.environ.get('CAPTURE_INTERVAL')))


# @app.route('/capturar')
# def perform():
#     if not capture.thread.is_alive():
#         capture.start()
#     else:
#         print("CAPTURA JA ESTA SENDO FEITA")
#     return redirect("/")

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        try:
            report_id = int(request.form['id'])
            report = Report.query.filter_by(id= report_id).first()
            db.session.delete(report)
            db.session.commit()
            print("Apagada captura de ", report.date)
        except Exception as e:
            print("Não foi possível apagar", e)
        
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
    


