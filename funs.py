from flask import request, json
import requests
from models import db, connect_db, Odds, User, Team, FavTeam, Book
import config

#########################################################
# get new odds for now


def new_odds():
    api_key = 'bf680b61288fa7d775ca603ec2c246ae'

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': config.api_key,
        'sport': 'basketball_nba',
        'region': 'us',  # uk | us | eu | au
        'mkt': 'h2h'  # h2h | spreads | totals
    })
    odds = Odds(spread=odds_response.text)
    db.session.add(odds)
    db.session.commit()
    return odds_response


def best_val(all_odds):
    """ Make array of highest value odds for each game """
    odds = json.loads(all_odds)
    home_highs = []
    away_highs = []
    # iterate through games and sites, then append max value to placeholder lists
    for game in odds['data']:
        hodds = []
        aodds = []
        for site in game['sites']:
            hodds.append(site['odds']['h2h'][0])
            aodds.append(site['odds']['h2h'][1])
        highest_home = max(hodds)
        highest_away = max(aodds)
        home_highs.append(highest_home)
        away_highs.append(highest_away)
    return home_highs, away_highs


def low_val(all_odds):
    """ Make array oflowest value odds for each game """
    odds = json.loads(all_odds)
    home_lows = []
    away_lows = []
    # iterate through games and sites, then append max value to placeholder lists
    for game in odds['data']:
        hodds = []
        aodds = []
        for site in game['sites']:
            hodds.append(site['odds']['h2h'][0])
            aodds.append(site['odds']['h2h'][1])
        highest_home = min(hodds)
        highest_away = min(aodds)
        home_lows.append(highest_home)
        away_lows.append(highest_away)
    return home_lows, away_lows


def add_avg_spread():
    """ Iterate through odds data to pass onto teamdata base. 
    After enough time will show true average  """
    count = Odds.query.count()
    odds = json.loads(Odds.query.get_or_404(count).spread)['data']
    for team in odds:
        hteam = team['teams'][0]
        ateam = team['teams'][1]
        htotal = 0
        atotal = 0
        for site in team['sites']:
            htotal += site['odds']['h2h'][0]
            atotal += site['odds']['h2h'][1]
        h_avg_total = round(htotal/len(team['sites']), 2)
        a_avg_total = round(atotal/len(team['sites']), 2)
        # psql storing ints not floats?
        home = Team.query.filter(Team.team_name == hteam).first()
        away = Team.query.filter(Team.team_name == ateam).first()
        if not home.entries:
            home.entries = 0
        if not away.entries:
            away.entries = 0
        home.entries += 1
        away.entries += 1
        if not home.totalOdds:
            home.totalOdds = 0
        if not away.totalOdds:
            away.totalOdds = 0
        home.totalOdds += h_avg_total
        away.totalOdds += a_avg_total

        db.session.add_all([home, away])
        db.session.commit()


def avg_book_place():
    # make this more efficient by doing avg rating within function and not adding each piece
    """ Add ranking of books price for each game """
    count = Odds.query.count()
    odds = json.loads(Odds.query.get_or_404(count).spread)['data']
    holder = []
    # split into invididual games, store in holder array
    for games in odds:
        holder.append(games['sites'])
    # take individual games and iterate through each betting sight for the game, then seperate for and away odds
    for game in holder:
        hodds = {}
        aodds = {}
        for site in game:
            hodds[site['site_key']] = site['odds']['h2h'][0]
            aodds[site['site_key']] = site['odds']['h2h'][1]
        sort_hodds = sorted(
            hodds.items(), key=lambda x: x[1], reverse=True)
        sort_aodds = sorted(
            aodds.items(), key=lambda x: x[1], reverse=True)
        # after making dictionary of an individual games home team odds for every sight, we sort those, then iterate through them to add their ranking to the DB
        if len(sort_hodds) > 5:
            for site in sort_hodds:
                rip = Book.query.filter(Book.book_name == site[0]).first()
                print(rip)
                if not rip.entries:
                    rip.entries = 0
                if not rip.avg_odds_count:
                    rip.avg_odds_count = 0
                rip.entries += 1
                rip.avg_odds_count += sort_hodds.index(site)

                db.session.add(rip)
                db.session.commit()
        if len(sort_aodds) > 5:
            for site in sort_aodds:
                rip = Book.query.filter(Book.book_name == site[0]).first()
                print(rip)
                if not rip.entries:
                    rip.entries = 0
                if not rip.avg_odds_count:
                    rip.avg_odds_count = 0
                rip.entries += 1
                rip.avg_odds_count += sort_aodds.index(site)
                # how can i make a unique placeholder to do one mass push to DB instead of 100 invidual pushes
                db.session.add(rip)
                db.session.commit()


def show_ranking():
    """ Get data from DB to get current book rankings """
    books = Book.query.all()
    ranks = {}
    for book in books:
        if book.entries:
            avg = book.avg_odds_count // book.entries
            ranks[book.book_name] = avg

    return {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1])}


def iterate_teams(odds):
    odds = json.loads(odds)['data']
    teams_playing = []
    for team in odds:
        teams_playing.append(team['teams'][0])
        teams_playing.append(team['teams'][1])
    return teams_playing


def rank_teams():
    """ rank teams """
    all_teams = Team.query.all()
    hold = {}
    for team in all_teams:
        if team.entries:
            hold[team.team_name] = team.totalOdds / team.entries
    return {k: v for k, v in sorted(hold.items(), key=lambda item: item[1])}
