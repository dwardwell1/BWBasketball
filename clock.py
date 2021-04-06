from funs import iterate_teams, new_odds, best_val, low_val, add_avg_spread, avg_book_place, show_ranking, rank_teams
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    new_odds()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
