"""Seed file to make sample data for db."""
import json
import requests
from models import User, Team, FavTeam, Book, Odds
from app import app, db
from example import results, test
from flask import jsonify


# Create all tables
db.drop_all()
db.create_all()

""" Create USers """
u1 = User(username='danny',
          password='faerts', over21=True)
u2 = User(username='Laura',
          password='nopers', over21=True)

db.session.add_all([u1, u2])

db.session.commit()

""" Create Teams """

t1 = Team(team_name='Atlanta Hawks',
          picture_url='https://cdn.iconscout.com/icon/free/png-256/atlanta-hawks-basketball-club-1880124-1593227.png')
t2 = Team(team_name='Boston Celtics',
          picture_url='https://assets-sports.thescore.com/basketball/team/1/logo.png')
t3 = Team(team_name='Brooklyn Nets',
          picture_url="https://assets-sports.thescore.com/basketball/team/2/logo.png")
t4 = Team(team_name='Charlotte Hornets',
          picture_url="https://basket88.com/wp-content/uploads/2019/10/charlotte-hornets-logo-128x128.png")
t5 = Team(team_name='Chicago Bulls',
          picture_url="https://i.pinimg.com/originals/4a/f1/a1/4af1a18b643f46292bd32cd18882e08d.png")
t6 = Team(team_name='Cleveland Cavaliers',
          picture_url="https://cdn.iconscout.com/icon/free/png-256/cleveland-cavaliers-1880119-1593202.png")
t7 = Team(team_name='Dallas Mavericks',
          picture_url="https://res-3.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1455216077/rwphyyufemjj6xxvl7wn.png")
t8 = Team(team_name='Denver Nuggets',
          picture_url="https://cdn.iconscout.com/icon/free/png-256/denver-nuggets-1880116-1593224.png")
t9 = Team(team_name='Detroit Pistons',
          picture_url="https://assets-sports.thescore.com/basketball/team/8/logo.png")
t10 = Team(team_name='Golden State Warriors',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/golden-state-warriors-1880115-1593223.png")
t11 = Team(team_name='Houston Rockets',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/houston-rockets-1880114-1593222.png")
t12 = Team(team_name='Indiana Pacers',
           picture_url="https://assets-sports.thescore.com/basketball/team/9/logo.png")
t13 = Team(team_name='Los Angeles Clippers',
           picture_url="https://assets-sports.thescore.com/basketball/team/17/logo.png")
t14 = Team(team_name='Los Angeles Lakers',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/los-angeles-lakers-1880111-1593200.png")
t15 = Team(team_name='Memphis Grizzlies',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/memphis-grizzlies-1880110-1593220.png")
t16 = Team(team_name='Miami Heat',
           picture_url="https://assets-sports.thescore.com/basketball/team/13/logo.png")
t17 = Team(team_name='Milwaukee Bucks',
           picture_url="https://assets-sports.thescore.com/basketball/team/10/logo.png")
t18 = Team(team_name='Minnesota Timberwolves',
           picture_url="https://assets-sports.thescore.com/basketball/team/27/logo.png")
t19 = Team(team_name='New Orleans Pelicans',
           picture_url="https://assets-sports.thescore.com/basketball/team/24/logo.png")
t20 = Team(team_name='New York Knicks',
           picture_url="https://i.pinimg.com/originals/29/31/56/2931561ee03378c821b805a21bbf3b87.png")
t21 = Team(team_name='Oklahoma City Thunder',
           picture_url="https://assets-sports.thescore.com/basketball/team/28/logo.png")
t22 = Team(team_name='Orlando Magic',
           picture_url="https://assets-sports.thescore.com/basketball/team/14/logo.png")
t23 = Team(team_name='Philadelphia 76ers',
           picture_url="https://assets-sports.thescore.com/basketball/team/4/logo.png")
t24 = Team(team_name='Phoenix Suns',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/phoenix-suns-1880101-1593212.png")
t25 = Team(team_name='Portland Trail Blazers',
           picture_url="https://assets-sports.thescore.com/basketball/team/29/logo.png")
t26 = Team(team_name='Sacramento Kings',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/sacramento-kings-1880099-1593210.png")
t27 = Team(team_name='San Antonio Spurs',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/san-antonio-spurs-1880098-1593209.png")
t28 = Team(team_name='Toronto Raptors',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/toronto-raptors-1880097-1593208.png")
t29 = Team(team_name='Utah Jazz',
           picture_url="https://assets-sports.thescore.com/basketball/team/30/small_logo.png")
t30 = Team(team_name='Washington Wizards',
           picture_url="https://cdn.iconscout.com/icon/free/png-256/washington-wizards-1880095-1593206.png")

db.session.add_all([t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14,
                    t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30])
db.session.commit()

""" Create Favteams """
ft1 = FavTeam(user_id=1, team_id=2)
ft2 = FavTeam(user_id=2, team_id=14)

db.session.add_all([ft1, ft2])
db.session.commit()

""" Create Books """

b1 = Book(book_name='pointsbetus',
          book_url='https://nj.pointsbet.com/', book_nice='PointsBet')
b2 = Book(book_name='fanduel',
          book_url='https://sportsbook.fanduel.com/sports', book_nice='FanDuel')
b3 = Book(book_name='williamhill_us',
          book_url='https://www.williamhill.com/us/', book_nice='William Hill')
b4 = Book(book_name='foxbet',
          book_url='https://www.foxbet.com/?no_redirect=1', book_nice='FoxBet')
b5 = Book(book_name='gtbets', book_url='https://m.gtbets.ag/', book_nice='GTBets')
b6 = Book(book_name='unibet',
          book_url='https://www.unibet.com/betting/sports/filter/basketball/nba', book_nice='UniBet')
b7 = Book(book_name='betrivers',
          book_url='https://www.betrivers.com/', book_nice='BetRivers')
b8 = Book(book_name='sugarhouse',
          book_url='https://www.playsugarhouse.com/', book_nice='SugarHouse')
b9 = Book(book_name='draftkings',
          book_url='https://sportsbook.draftkings.com/leagues/basketball/103?category=game-lines&subcategory=game', book_nice='DraftKings')
b10 = Book(book_name='betmgm',
           book_url='https://promo.nj.betmgm.com/en/promo/geolocator?orh=sports.betmgm.com', book_nice='BetMGM')
b11 = Book(book_name='caesars',
           book_url='https://www.caesarscasino.com/sports/', book_nice='Caesars')
b12 = Book(book_name='mybookieag',
           book_url='https://mybookie.ag/sportsbook/', book_nice='MyBookie.ag')
b13 = Book(book_name='betfair',
           book_url='https://www.betfair.com/sport/', book_nice='BetFair')
b14 = Book(book_name='lowvig', book_url='https://www.lowvig.ag/',
           book_nice='LowVig.ag')
b15 = Book(book_name='betonlineag',
           book_url='https://www.betonline.ag/sportsbook')
b16 = Book(book_name='bookmaker',
           book_url='https://www.bookmaker.eu/sportsbook',
           book_nice='Bookmaker')
b17 = Book(book_name='bovada',
           book_url='https://www.bovada.lv/sports/basketball',
           book_nice='Bovada')
b18 = Book(book_name='intertops', book_url='https://sports.intertops.eu/',
           book_nice='Intertops')


db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10,
                    b11, b12, b13, b14, b15, b16, b17, b18])
db.session.commit()


odds = Odds(spread=test)
db.session.add(odds)
db.session.commit()
""" Fetch Odds """


# def new_odds():
#     api_key = 'bf680b61288fa7d775ca603ec2c246ae'

#     odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
#         'api_key': api_key,
#         'sport': 'basketball_nba',
#         'region': 'us',  # uk | us | eu | au
#         'mkt': 'h2h'  # h2h | spreads | totals
#     })
#     odds = Odds(spread=odds_response.text)
#     db.session.add(odds)
#     db.session.commit()


# new_odds()
