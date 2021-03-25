from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length

teams = [("", '--'), (1, 'Atlanta Hawks'), (2, 'Boston Celtics'), (3, 'Brooklyn Nets'), (4, 'Charlotte Hornets'), (5, 'Chicago Bulls'), (6, 'Cleveland Cavaliers'), (7, 'Dallas Mavericks'), (8, 'Denver Nuggets'), (9, 'Detroit Pistons'), (10, 'Golden State Warriors'), (11, 'Houston Rockets'), (12, 'Indiana Pacers'), (13, 'Los Angeles Clippers'), (14, 'Los Angeles Lakers'), (15, 'Memphis Grizzlies'),
         (16, 'Miami Heat'), (17, 'Milwaukee Bucks'), (18, 'Minnesota Timberwolves'), (19, 'New Orleans Pelicans'), (20, 'New York Knicks'), (21, 'Oklahoma City Thunder'), (22, 'Orlando Magic'), (23, 'Philadelphia 76ers'), (24, 'Phoenix Suns'), (25, 'Portland Trail Blazers'), (26, 'Sacramento Kings'), (27, 'San Antonio Spurs'), (28, 'Toronto Raptors'), (29, 'Utah Jazz'), (30, 'Washington Wizards')]


class UserAddForm(FlaskForm):
    """ Form For Adding Users """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    over21 = BooleanField('Over 21?')
    fav_one = SelectField('Favorite Team?', choices=teams)
    fav_two = SelectField('Second Favorite?', choices=teams)
    fav_three = SelectField('Third Favorite?', choices=teams)


class LoginForm(FlaskForm):
    """ Login Form """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
