from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job("interval", minutes=20)
def timed_job():
    url = "https://nycu-cs-credits-stimulator.herokuapp.com/"
    requests.get(url)
    print("Send request to", url)

sched.start()