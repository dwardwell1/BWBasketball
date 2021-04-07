
from funs import iterate_teams, new_odds, best_val, low_val, add_avg_spread, avg_book_place, show_ranking, rank_teams
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import current_app as app

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=35)
def timed_job():
    new_odds()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=36)
def scheduled_job():
    add_avg_spread()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=7)
def scheduled_job2():
    avg_book_place()


sched.start()
