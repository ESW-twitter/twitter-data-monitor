import os
import redis
from rq import Worker, Queue, Connection
from __init__ import generate_csv_report

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
