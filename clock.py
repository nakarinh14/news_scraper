from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from factory import scrape
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

def gather_news():
    q.enqueue(scrape)

# def remove_news():
#  q.enqueue(run_gather_comments)


sched.add_job(gather_news)
sched.add_job(gather_news, 'interval', minutes=5)

sched.start()