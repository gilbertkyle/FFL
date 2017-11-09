from flask import Flask, render_template, request, redirect, url_for, flash, g, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user, UserMixin
from forms import RegistrationForm, LoginForm, choices, LeagueForm, JoinLeagueForm, CreateLeagueForm, PickForm, league_weeks
from werkzeug import generate_password_hash, check_password_hash
from password import my_password, my_development_key, my_username, my_hostname, my_database



app = Flask(__name__)
app.secret_key = my_development_key
app.config["DEBUG"] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Sets up the database. This is specific to pythonanywhere.com


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{database}".format(
    username= my_username,
    password= my_password,
    hostname= my_hostname,
    database= my_database,
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)
metadata = db.MetaData()



class League(db.Model):

    __tablename__ = "leagues"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    admin = db.Column(db.String(40))
    password = db.Column(db.String(150))
    players = db.relationship("User", backref="league", lazy="dynamic")

    def __init__(self, name, admin, password):
        self.name = name
        self.admin = admin
        self.password = password


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    password = db.Column(db.String(150))
    email = db.Column(db.String(60))
    username = db.Column(db.String(30), unique=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))

    def __init__(self, first_name, last_name, password, email, username):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.username = username

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)





class Pick(db.Model):

    __tablename__ = "picks"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    league = db.Column(db.String(20))
    week = db.Column(db.Integer)
    year = db.Column(db.Integer)
    quarterback = db.Column(db.String(20))
    qb_points = db.Column(db.Float)
    running_back = db.Column(db.String(20))
    rb_points = db.Column(db.Float)
    wide_receiver = db.Column(db.String(20))
    wr_points = db.Column(db.Float)
    tight_end = db.Column(db.String(20))
    te_points = db.Column(db.Float)
    defense = db.Column(db.String(20))
    defense_points = db.Column(db.Float)

    def __init__(self, username, league, week, year, quarterback, running_back, wide_receiver, tight_end, defense):
        self.username = username
        self.league = league
        self.week = week
        self.year = year
        self.quarterback = quarterback
        self.qb_points = 0.0
        self.running_back = running_back
        self.rb_points = 0.0
        self.wide_receiver = wide_receiver
        self.wr_points = 0.0
        self.tight_end = tight_end
        self.te_points = 0.0
        self.defense = defense
        self.defense_points = 0.0

class Player(db.Model):

    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    year = db.Column(db.Integer)
    week = db.Column(db.Integer)
    position = db.Column(db.String(5))
    fantasy_points = db.Column(db.Float)
    passing_yds = db.Column(db.Integer)
    passing_tds = db.Column(db.Integer)
    passing_int = db.Column(db.Integer)
    rushing_yds = db.Column(db.Integer)
    rushing_tds = db.Column(db.Integer)
    receiving_yds = db.Column(db.Integer)
    receiving_tds = db.Column(db.Integer)
    kickret_tds = db.Column(db.Integer)
    two_point_conversions = db.Column(db.Integer)
    fumbles_lost = db.Column(db.Integer)
    fumbles_rec_tds = db.Column(db.Integer)

    def __init__(self, name, year, week, position, fantasy_points, passing_yds, passing_tds, passing_int, rushing_yds, rushing_tds, receiving_yds, receiving_tds, kickret_tds, two_point_conversions, fumbles_lost, fumbles_rec_tds):
        self.name = name
        self.year = year
        self.week = week
        self.position = position
        self.fantasy_points = fantasy_points
        self.passing_yds = passing_yds
        self.passing_tds = passing_tds
        self.passing_int = passing_int
        self.rushing_yds = rushing_yds
        self.rushing_tds = rushing_tds
        self.receiving_yds = receiving_yds
        self.receiving_tds = receiving_tds
        self.kickret_tds = kickret_tds
        self.two_point_conversions = two_point_conversions
        self.fumbles_lost = fumbles_lost
        self.fumbles_rec_tds = fumbles_rec_tds

    @property
    def serialize(self):
        return {
            "name" : self.name,
            }

class Defense(db.Model):

    __tablename__ = "defense"

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    week = db.Column(db.Integer)
    year = db.Column(db.Integer)
    points_allowed = db.Column(db.Integer)
    fantasy_points = db.Column(db.Float)
    """sacks = db.Column(db.Float)
    interceptions = db.Column(db.Integer)
    fumble_recoveries = db.Column(db.Integer)
    defense_tds = db.Column(db.Integer)
    kicks_blocked = db.Column(db.Integer)
    kickret_tds = db.Column(db.Integer)
    puntret_tds = db.Column(db.Integer)"""

    def __init__(self, team, week, year, points_allowed, fantasy_points):
        self.team = team
        self.week = week
        self.year = year
        self.points_allowed = points_allowed
        self.fantasy_points = fantasy_points
        """self.sacks = sacks
        self.interceptions = interceptions
        self.fumble_recoveries = fumble_recoveries
        self.defense_tds = defense_tds
        self.kicks_blocked = kicks_blocked
        self.kickret_tds = kickret_tds
        self.puntret_tds = puntret_tds"""



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def layout():
    return render_template("layout.html")



@app.route('/index')
def index():
    if current_user.is_authenticated:
        picks = Pick.query.filter_by(username=current_user.username).all()

        picks.sort(key=lambda x: x.week)  #Sorts the picks by week
        for pick in picks:

            # Picks the player with the most points out of all the players with the same first initial and last name. Not really a better way to do this.

            qb = Player.query.filter_by(name=pick.quarterback, week=pick.week, year=2017).order_by(Player.fantasy_points.desc()).first()
            rb = Player.query.filter_by(name=pick.running_back, week=pick.week, year=2017).order_by(Player.fantasy_points.desc()).first()
            wr = Player.query.filter_by(name=pick.wide_receiver, week=pick.week, year=2017).order_by(Player.fantasy_points.desc()).first()
            te = Player.query.filter_by(name=pick.tight_end, week=pick.week, year=2017).order_by(Player.fantasy_points.desc()).first()
            df = Defense.query.filter_by(team=pick.defense, week=pick.week, year=2017).order_by(Defense.fantasy_points.desc()).first()

            pick.qb_points = qb.fantasy_points if qb else 0.0
            pick.rb_points = rb.fantasy_points if rb else 0.0
            pick.wr_points = wr.fantasy_points if wr else 0.0
            pick.te_points = te.fantasy_points if te else 0.0
            pick.defense_points = df.fantasy_points if df else 0.0

            db.session.commit()


        return render_template("index.html", picks=picks)

    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)

    if request.method == "POST" and form.validate():
        hash = generate_password_hash(str(form.password.data))
        user = User(form.first_name.data, form.last_name.data, hash, form.email.data, form.username.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering")
        return redirect(url_for("login"))


    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        match = check_password_hash(user.password, password)
        if not match:
            flash("Invalid password.")
            return redirect(url_for("login"))
        if user is None:
            flash("Invalid email or password")
            return redirect(url_for("login"))
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("index"))


    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/picks', methods=["GET", "POST"])
@login_required
def picks():
    form = PickForm(request.form)
    week = dict(choices).get(form.week.data)
    if request.method == "POST" and form.validate():

        # If there is a duplicate pick, don't allow it to happen.


        # If there is already a pick that week by the current user, delete that row

        if Pick.query.filter_by(week=week, username=current_user.username):
            Pick.query.filter_by(week=week, username=current_user.username).delete()
            db.session.commit()
        picks = Pick(current_user.username, current_user.league_id, week, 2017, form.quarterback.data,
                form.running_back.data, form.wide_receiver.data, form.tight_end.data, form.defense.data)


        db.session.add(picks)
        db.session.commit()
        return redirect(url_for("index"))

    # This is a list of players you have already picked from all weeks besides the current week, so you can repick players from your current week

    my_players = []
    picks = Pick.query.filter(Pick.username==current_user.username).filter(Pick.week != week).all()
    for pick in picks:
        my_players.append(pick.quarterback)
        my_players.append(pick.running_back)
        my_players.append(pick.wide_receiver)
        my_players.append(pick.tight_end)
        my_players.append(pick.defense)


    # These lists are used for the twitter typeahead function for each position

    quarterbacks = []
    all_qbs = Player.query.filter_by(position="QB", year=2017).all()
    for player in all_qbs:
        quarterbacks.append(player.name)
    quarterbacks = list(set(quarterbacks))

    running_backs = []
    all_rbs = Player.query.filter_by(position="RB", year=2017).all()
    for player in all_rbs:
        running_backs.append(player.name)
    running_backs = list(set(running_backs))

    wide_receivers = []
    all_wrs = Player.query.filter_by(position="WR", year=2017).all()
    for player in all_wrs:
        wide_receivers.append(player.name)
    wide_receivers = list(set(wide_receivers))

    tight_ends = []
    all_tes = Player.query.filter_by(position="TE", year=2017).all()
    for player in all_tes:
        tight_ends.append(player.name)
    tight_ends = list(set(tight_ends))

    defense = []
    all_defense = Defense.query.all()
    for d in all_defense:
        defense.append(d.team)
    defense = list(set(defense))

    return render_template("picks.html", form=form, defense=defense, quarterbacks=quarterbacks, running_backs=running_backs, wide_receivers=wide_receivers, tight_ends=tight_ends, my_players=my_players)

@app.route('/league', methods=["GET", "POST"])
@login_required
def league():
    form = LeagueForm(request.form)
    week = dict(choices).get(form.week.data)
    if request.method == "POST" and form.validate():

        users_with_picks = []
        users_without_picks = []
        picks = Pick.query.filter_by(week=week, league=current_user.league_id)
        users = User.query.filter_by(league_id=current_user.league_id)


        for pick in picks:
            users_with_picks.append(pick.username)
        for user in users:
            if user.username not in users_with_picks:
                users_without_picks.append(user.username)
        picks = Pick.query.filter_by(week=week, league=current_user.league_id)
        return render_template("league_picks.html", picks=picks, week=week, users=users, users_without_picks=users_without_picks)

    return render_template("league.html", form=form)


@app.route('/join_league', methods=["GET", "POST"])
@login_required
def join_league():
    form = JoinLeagueForm(request.form)
    if current_user.league_id is None:
        if request.method == "POST" and form.validate:
            user = User.query.filter_by(username=current_user.username).first()
            league = League.query.filter_by(name=form.league.data).first()
            if check_password_hash(league.password, form.password.data):
                user.league_id = league.id
                db.session.commit()
            return redirect(url_for("league"))
    return render_template("join_league.html", form=form)


@app.route('/create_league', methods=["GET", "POST"])
@login_required
def create_league():
    form = CreateLeagueForm(request.form)
    user = User.query.filter_by(username=current_user.username).first()
    league = League.query.filter_by(name=form.league.data).first()
    if request.method == "POST" and form.validate() and not league:
        hash = generate_password_hash(form.password.data)
        new_league = League(form.league.data, current_user.username, hash)
        db.session.add(new_league)
        league = League.query.filter_by(name=form.league.data).first()
        user.league_id = league.id
        db.session.commit()
        return render_template("index.html")
    return render_template("create_league.html", form=form)




@app.route('/leaderboards', methods=["GET", "POST"])
@login_required
def leaderboards():
    #picks = db.session.query(Pick).all()

    picks = db.session.query(Pick.username, db.func.sum(Pick.qb_points + Pick.rb_points + Pick.wr_points + Pick.te_points + Pick.defense_points)).group_by(Pick.username).all()
    return render_template("leaderboards.html", picks=picks)






@app.route('/_search_player', methods=["GET", "POST"])
def search_player():
    if not request.args.get('search'):
        raise RuntimeError("missing argument")
    search = request.args.get('search')
    players = Player.query.filter(Player.name.like("%" + search + "%")).all()
    return jsonify(json_list=[player.serialize for player in players])

@app.route('/_search_defense', methods=["GET"])
def search_defense():
    defense = Defense.query.all()
    return jsonify(json_list=[defense.serialize for d in defense])


@app.before_request
def before_request():
    g.user = current_user



if __name__ == "__main__":
    app.run()
