from modules.twitter_user import TwitterUser
from apscheduler.schedulers.blocking import BlockingScheduler
from __init__ import csv_report

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=60)
def generate_reports():
    print("Generating reports...")
    capture = csv_report()
    capture.start()
    print("Done ")

sched.start()
