from flask import Flask, request, render_template,  redirect, flash, session, jsonify, json
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Odds, User, Team, FavTeam, Book
import re


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "bbqchicken"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

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

#########################################################
# route logic


@app.route('/')
def home_page():
    """Render home page"""
    all_odds = Odds.query.get_or_404(1).spread
    return render_template("home.html", odds=json.loads(all_odds))


#########################################################
# API logic


@app.route('/api/odds')
def get_all_odds():
    """ Get all odds JSON """
    all_odds = Odds.query.get_or_404(1).spread
    return jsonify(odds=all_odds)


def capital_words_spaces(str1):
    # move this function later
    """ Seperate team url for API search """
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)


@app.route('/api/odds/<team>')
def get_team_odds(team):
    """ Get specific teams odds for that slate of games """
    team = capital_words_spaces(team)
    all_odds = json.loads(Odds.query.get_or_404(1).spread)
    for game in all_odds['data']:
        if team in game['teams']:
            return jsonify(game)
    return jsonify('No games')

###############################################################
# Functions


def add_avg_spread():
    """ Iterate through odds data to pass onto teamdata base. 
    After enough time will show true average  """
    odds = json.loads(Odds.query.get_or_404(1).spread)['data']
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
    """ Add ranking of books price for each game """
    odds = json.loads(Odds.query.get_or_404(1).spread)['data']
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
        for site in sort_hodds:
            rip = Book.query.filter(Book.book_name == site[0]).first()
            print(rip)
            if not rip.entries:
                rip.entries = 0
            if not rip.avg_odds_count:
                rip.avg_odds_count = 0
            rip.entries += 1
            rip.avg_odds_count += sort_hodds.index(site)
            # how can i make a unique placeholder to do one mass push to DB instead of 100 invidual pushes
            db.session.add(rip)
            db.session.commit()
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
    return ranks
