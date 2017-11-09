from wtforms import TextField, PasswordField, SubmitField, SelectField, Form, validators
from datetime import datetime, timedelta


base = datetime(2017, 9, 3, 17, 0, 0)
today = datetime.now()
diff = today - base

league_weeks = int(diff.days/7)
league_choices = [(f, str(f)) for f in range(1, league_weeks+1)]
pick_choices = [(f, str(f)) for f in range(league_weeks+1, 18)]


choices = [(f, str(f)) for f in range(2, 18)]

class RegistrationForm(Form):
    first_name = TextField("First name", [validators.Required("Please enter your first name.")])
    last_name = TextField("Last name", [validators.Required("Please enter your first name.")])
    email = TextField("Email", [validators.Required("Please enter your e-mail address."), validators.Email("Please enter your email address.")])
    password = PasswordField("Password", [validators.Required("Please enter a password."), validators.EqualTo('confirm', message='passwords must match')])
    confirm = PasswordField("Repeat Password")
    username = TextField("Username", [validators.Required("Please enter a username")])
    submit = SubmitField("Create an Account")

class PickForm(Form):
    week = SelectField("Week", coerce=int, choices=pick_choices)
    quarterback = TextField("Quarterback", [validators.Required("You need a Quarterback")])
    running_back = TextField("Running Back", [validators.Required("You need a Running Back")])
    wide_receiver = TextField("Wide Receiver", [validators.Required("You need a Wide Receiver")])
    tight_end = TextField("Tight End", [validators.Required("You need a Tight End")])
    defense = TextField("Defense", [validators.Required("You need a Defense")])
    submit = SubmitField("Submit your picks")



class LoginForm(Form):
    username = TextField("Username", [validators.Required("Enter username")])
    password = PasswordField("Password", [validators.Required("Enter password")])
    submit = SubmitField("Login")

class LeagueForm(Form):
    week = SelectField("Week", coerce=int, choices=league_choices)

class JoinLeagueForm(Form):
    league = TextField("League", [validators.Required("Enter a league to join")])
    password = PasswordField("Password", [validators.Required("Enter a password")])

class CreateLeagueForm(Form):
    league = TextField("League", [validators.Required("Enter a name for your league")])
    password = PasswordField("Password", [validators.Required("Enter a password"), validators.EqualTo('confirm', message='passwords must match')])
    confirm = PasswordField("Repeat Password")
