from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from app import db
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    password = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    username = db.Column(db.String(30), unique=True)
    #picks = db.relationship("Pick", backref="users", lazy="dynamic")

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

    def __init__(self, username, league, week, quarterback, running_back, wide_receiver, tight_end, defense):
        self.username = username
        self.league = league
        self.week = week
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

class Defense(db.Model):

    __tablename__ = "defense"

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(20))
    week = db.Column(db.Integer)
    points_allowed = db.Column(db.Integer)
    fantasy_points = db.Column(db.Float)
    """sacks = db.Column(db.Float)
    interceptions = db.Column(db.Integer)
    fumble_recoveries = db.Column(db.Integer)
    defense_tds = db.Column(db.Integer)
    kicks_blocked = db.Column(db.Integer)
    kickret_tds = db.Column(db.Integer)
    puntret_tds = db.Column(db.Integer)"""

    def __init__(self, team, week, points_allowed, fantasy_points):
        self.team = team
        self.week = week
        self.points_allowed = points_allowed
        self.fantasy_points = fantasy_points
        """self.sacks = sacks
        self.interceptions = interceptions
        self.fumble_recoveries = fumble_recoveries
        self.defense_tds = defense_tds
        self.kicks_blocked = kicks_blocked
        self.kickret_tds = kickret_tds
        self.puntret_tds = puntret_tds"""