from funs import iterate_teams, new_odds, best_val, low_val, add_avg_spread, avg_book_place, show_ranking, rank_teams
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=15)
def timed_job():
    new_odds()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=16)
def scheduled_job():
    add_avg_spread()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=9, minute=18)
def scheduled_job2():
    avg_book_place()


sched.start()
