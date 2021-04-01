
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
    password = db.Column(db.Text, nullable=False)
    over21 = db.Column(db.Boolean, nullable=False)

    @classmethod
    def signup(cls, username,  password, over21):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            over21=over21
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


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
    teams = db.relationship('Team', backref='favTeam')

# left off here to make easier relationship to pull up favorite teams! by name so not so many dbs!!!!!


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
