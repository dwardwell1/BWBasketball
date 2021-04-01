from flask import Flask, request, render_template,  redirect, flash, session, jsonify, json, g, session
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Odds, User, Team, FavTeam, Book
import re
from sqlalchemy.exc import IntegrityError
from forms import *
from funs import new_odds, best_val, low_val
import time
import datetime

dt = datetime.datetime.now()
# dt.strftime('%X')
# datetime.datetime.utcfromtimestamp(1616890000)

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "bbqchicken"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def add_user():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            if form.over21.data == False:
                return render_template('home.html')
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                over21=form.over21.data)

            db.session.commit()

            favteam = FavTeam(
                user_id=user.id,
                team_id=form.fav_one.data
            )
            db.session.add(favteam)
            if form.fav_two.data:
                fav2 = FavTeam(
                    user_id=user.id,
                    team_id=form.fav_two.data)
                db.session.add(fav2)
            if form.fav_three.data:
                fav3 = FavTeam(
                    user_id=user.id,
                    team_id=form.fav_three.data)
                db.session.add(fav3)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/odds")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash(f"Goodbye!", "success")
    return redirect("/")


@app.route('/edit', methods=["GET", "POST"])
def edit():
    """ Edit Profile """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user_id = g.user.id

    form = EditUser(obj=g.user)

    fav_teams = FavTeam.query.filter(FavTeam.user_id == user_id).all()

    if form.validate_on_submit():
        g.user.username = form.username.data
        db.session.commit()
        if fav_teams[0] and form.fav_one.data:
            fav_teams[0].team_id = form.fav_one.data
            db.session.commit()
        elif form.fav_one.data:
            favteam = FavTeam(
                user_id=user_id,
                team_id=form.fav_one.data
            )
            db.session.add(favteam)
            db.session.commit()
        if fav_teams[1] and form.fav_two.data:
            fav_teams[1].team_id = form.fav_two.data
            db.session.commit()
        elif form.fav_two.data:
            favteam2 = FavTeam(
                user_id=user_id,
                team_id=form.fav_two.data
            )
            db.session.add(favteam2)
            db.session.commit()
        if fav_teams[2] and form.fav_three.data:
            fav_teams[2].team_id = form.fav_two.data
            db.session.commit()
        elif form.fav_three.data:
            favteam3 = FavTeam(
                user_id=user_id,
                team_id=form.fav_three.data
            )
            db.session.add(favteam3)
            db.session.commit()

        return redirect('/myteams')

    return render_template('edit.html', form=form)


#########################################################
# route logic


@app.route('/')
def home_page():
    """Render home page"""
    count = Odds.query.count()
    all_odds = Odds.query.get_or_404(count).spread
    teams = Team.query.all()
    user = g.user
    return render_template("home.html", odds=json.loads(all_odds), pics=teams, user=user)


@app.route('/odds')
def odds_page():
    """Render home page"""
    count = Odds.query.count()
    all_odds = Odds.query.get_or_404(count).spread
    teams = Team.query.all()
    best_home_values = best_val(all_odds)[0]
    best_away_values = best_val(all_odds)[1]
    worst_home_values = low_val(all_odds)[0]
    worst_away_values = low_val(all_odds)[1]

    return render_template("display.html", odds=json.loads(all_odds), pics=teams, bestHome=best_home_values, bestAway=best_away_values, worstHome=worst_home_values, worstAway=worst_away_values)


@app.route('/myteams')
def team_odds():
    """ API call to see just favorited Teams """

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user_id = g.user.id
    fav_teams = FavTeam.query.filter(FavTeam.user_id == user_id).all()
    team_ids = []
    for team in fav_teams:
        team_ids.append(team.teams.team_name)
    teams = Team.query.all()
    count = Odds.query.count()
    all_odds = Odds.query.get_or_404(count).spread
    best_home_values = best_val(all_odds)[0]
    best_away_values = best_val(all_odds)[1]
    worst_home_values = low_val(all_odds)[0]
    worst_away_values = low_val(all_odds)[1]
    teams_playing = iterate_teams(all_odds)

    return render_template("myteams.html", odds=json.loads(all_odds), pics=teams, bestHome=best_home_values, bestAway=best_away_values, worstHome=worst_home_values, worstAway=worst_away_values, teams=team_ids, playing=teams_playing)
    # changing db relationbship so I can get team names to iterate through


@app.route('/bookranks')
def books_ranks():
    """ Show Book Ranking """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    ranks = show_ranking()

    return render_template('bookranks.html', ranks=ranks)


@app.route('/teamranks')
def team_ranks():
    """ Show ranking of teams based on average spread """
    ranked = rank_teams()

    return render_template('teamranks.html', teams=ranked)

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


# test

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


@app.context_processor
def inject_today_date():
    def get_time(game_time):
        test = datetime.datetime.utcfromtimestamp(
            game_time)
        return datetime.datetime.fromtimestamp(game_time).strftime('%m-%d %H:%M')
    return dict(get_time=get_time)
