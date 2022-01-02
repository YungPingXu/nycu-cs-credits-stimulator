from apscheduler.schedulers.blocking import BlockingScheduler
import urllib

sched = BlockingScheduler()

@sched.scheduled_job("cron", minute="*/2")
def scheduled_job():
    url = "https://nycu-cs-credits-stimulator.herokuapp.com/"
    urllib.request.urlopen(url)
    print("Send request to https://nycu-cs-credits-stimulator.herokuapp.com/")

sched.start()