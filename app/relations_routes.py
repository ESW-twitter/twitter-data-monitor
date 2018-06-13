#coding: utf-8
from app import app, db
from app.models import RelationReport, TLRelationReport
from app.scheduler import scheduler, reschedule_job, retrieve_interval, retrieve_next_runtime
from flask import Flask, make_response, request, render_template, redirect



@app.route('/relacoes/mudarintervalo', methods=['POST'])
def relations_change_interval():
    if request.method == 'POST':
        minutes = int(request.form['intervalo'])
        reschedule_job(id='relations', minutes=minutes)    

    return redirect("/relacoes/")


@app.route('/relacoes/')
def relations():
    
    interval = retrieve_interval('relations')
    next_run = retrieve_next_runtime('relations') 
    
    reports = RelationReport.query.all()
    timeline_reports = TLRelationReport.query.all()

    return render_template('relacoes.html', reports=reports, tl_reports = timeline_reports, intervalo=interval, next=next_run)

@app.route('/relacoes/delete', methods=['POST'])
def relations_delete():
    if request.method == 'POST':
        try:
            report_id = int(request.form['id'])
            report = RelationReport.query.filter_by(id= report_id).first()
            db.session.delete(report)
            db.session.commit()
            print("Apagada captura de ", report.date)
        except Exception as e:
            print("Não foi possível apagar", e)
        
    return redirect("/relacoes/")

@app.route('/relacoes/download_csv/<rid>')
def relacoes_download_csv(rid):
    report = RelationReport.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format("Relacoes-"+report.date+"_"+report.hour)
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response

@app.route('/tlrelacoes/download_csv/<rid>')
def timeline_relacoes_download_csv(rid):
    report = TLRelationReport.query.filter_by(id= rid).first()
    csv = report.csv_content.decode()
    response = make_response(csv)
    cd = 'attachment; filename={}.csv'.format("Relacoes-semanais-"+report.date+"_"+report.hour)
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response





