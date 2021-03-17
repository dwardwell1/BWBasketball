
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

# datetime.utcnow()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Create Users Table """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    over21 = db.Column(db.Boolean, nullable=False)


class Team(db.Model):
    """ Create Teams table """
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.Text, nullable=False,  unique=True)
    team_url = db.Column(db.Text)
    picture_url = db.Column(db.Text,  unique=True)
    entries = db.Column(db.Integer)
    totalOdds = db.Column(db.Float)


class FavTeam(db.Model):
    """ Relationship table for users favorite teams, whats this called again """
    __tablename__ = 'fav_teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))


class Book(db.Model):
    """ List of books and their stats  """

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.Text, nullable=False, unique=True)
    book_url = db.Column(db.Text)
    picture_url = db.Column(db.Text,  unique=True)
    avg_odds_count = db.Column(db.Integer)
    entries = db.Column(db.Integer)


class Odds(db.Model):

    __tablename__ = 'odds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spread = db.Column(db.JSON, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())
