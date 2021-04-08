
from funs import iterate_teams, new_odds, best_val, low_val, add_avg_spread, avg_book_place, show_ranking, rank_teams
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import current_app
from app import app

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=10)
def timed_job():
    with app.app_context():
        new_odds()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=12)
def scheduled_job():
    with app.app_context():
        add_avg_spread()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=13)
def scheduled_job2():
    with app.app_context():
        avg_book_place()


sched.start()
