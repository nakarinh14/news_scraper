from apscheduler.schedulers.blocking import BlockingScheduler
from factory import scrape
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    scrape()

sched.start()