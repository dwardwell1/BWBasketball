from flask import request, json
import requests
from models import db, connect_db, Odds, User, Team, FavTeam, Book

#########################################################
# get new odds for now


def new_odds():
    api_key = 'bf680b61288fa7d775ca603ec2c246ae'

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': api_key,
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
