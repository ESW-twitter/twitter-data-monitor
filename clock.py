import os
from modules.twitter_user import TwitterUser
from apscheduler.schedulers.blocking import BlockingScheduler
from __init__ import csv_report

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes= int(os.environ.get('CAPTURE_INTERVAL')) )
def generate_reports():
    print("Generating reports...")
    capture = csv_report()
    capture.start()
    print("Done ")

sched.start()
