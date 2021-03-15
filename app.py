from flask import Flask, request, render_template,  redirect, flash, session, jsonify, json
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


@app.route('/')
def home_page():
    """Render home page"""
    all_odds = Odds.query.get_or_404(1).spread
    return render_template("home.html", odds=json.loads(all_odds))


@app.route('/api/odds')
def get_odds():
    all_odds = Odds.query.all()
    return all_odds, 200
