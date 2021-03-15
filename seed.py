"""Seed file to make sample data for db."""
import json
import requests
from models import User, Team, FavTeam, Book, Odds
from app import app, db

api_key = 'bf680b61288fa7d775ca603ec2c246ae'

odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,
    'sport': 'basketball_nba',
    'region': 'us',  # uk | us | eu | au
    'mkt': 'h2h'  # h2h | spreads | totals
})
# Create all tables
db.drop_all()
db.create_all()

""" Create USers """
u1 = User(username='danny', email='dwardwell1@gmail.com',
          password='faerts', over21=True)
u2 = User(username='Laura', email='laura@gmail.com',
          password='nope', over21=True)

db.session.add_all([u1, u2])

db.session.commit()

""" Create Teams """

t1 = Team(team_name='Atlanta Hawks')
t2 = Team(team_name='Boston Celtics')
t3 = Team(team_name='Brooklen Nets')
t4 = Team(team_name='Charlotte Hornets')
t5 = Team(team_name='Chicago Bulls')
t6 = Team(team_name='Cleveland Cavaliers')
t7 = Team(team_name='Dallas Mavericks')
t8 = Team(team_name='Denver Nuggets')
t9 = Team(team_name='Detroit Pistons')
t10 = Team(team_name='Golden State Warriors')
t11 = Team(team_name='Houston Rockets')
t12 = Team(team_name='Indiana Pacers')
t13 = Team(team_name='Los Angeles Clippers')
t14 = Team(team_name='Lost Angeles Lakers')
t15 = Team(team_name='Memphis Grizzlies')
t16 = Team(team_name='Miami Heat')
t17 = Team(team_name='Milwaukee Bucks')
t18 = Team(team_name='Minnesota Timberwolves')
t19 = Team(team_name='New Orleans Pelicans')
t20 = Team(team_name='New York Knicks')
t21 = Team(team_name='Oklahoma City Thunder')
t22 = Team(team_name='Orlando Magic')
t23 = Team(team_name='Philadelphia 76ers')
t24 = Team(team_name='Phoenix Suns')
t25 = Team(team_name='Portland Trail Blazers')
t26 = Team(team_name='Sacramento Kings')
t27 = Team(team_name='San Antonio Spurs')
t28 = Team(team_name='Toronto Raptors')
t29 = Team(team_name='Utah Jazz')
t30 = Team(team_name='Washington Wizards')

db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14,
                    t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30])
db.session.commit()

""" Create Favteams """
ft1 = FavTeam(user_id=1, team_id=2)
ft2 = FavTeam(user_id=2, team_id=14)

db.session.add_all([ft1, ft2])
db.session.commit()

""" Create Books """

b1 = Book(book_name='pointsbetus')
b2 = Book(book_name='fanduel')
b3 = Book(book_name='williamhill_us')
b4 = Book(book_name='foxbet')
b5 = Book(book_name='gtbets')
b6 = Book(book_name='unibet')
b7 = Book(book_name='betrivers')
b8 = Book(book_name='sugarhouse')
b9 = Book(book_name='draftkings')
b10 = Book(book_name='betmgm')
b11 = Book(book_name='caesars')
b12 = Book(book_name='mybookieag')
b13 = Book(book_name='betfair')

db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13])
db.session.commit()

""" Fetch Odds """

odds = Odds(spread=odds_response.text)
db.session.add(odds)
db.session.commit()
