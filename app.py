from flask import Flask, request, render_template,  redirect, flash, session, jsonify, json
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Odds, User, Team, FavTeam, Book


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


@app.route('/api/odds')
def get_odds():
    all_odds = Odds.query.all()
    return all_odds, 200


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


def test(int):
    test = Team.query.get_or_404(int)
    print(test.totalOdds)
