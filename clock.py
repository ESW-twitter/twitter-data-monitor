import os
from modules.twitter_user import TwitterUser
from apscheduler.schedulers.blocking import BlockingScheduler
from __init__ import csv_report

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes= os.environ.get('CAPTURE_INTERVAL'))
def generate_reports():
    print("Generating reports...")
    csv_report()
    print("Done ")

sched.start()
