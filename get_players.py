#! /user/bin/python2.7

import nflgame
from flask_sqlalchemy import SQLAlchemy

from app import db
from app import Player, Defense

def update_picks(year, week):

    engine = db.engine
    connection = engine.connect()

    quarterbacks = connection.execute("""UPDATE picks, players
                                            SET picks.qb_points=(
                                                SELECT IFNULL(MAX(p.fantasy_points), 0) FROM (
                                                    SELECT * FROM players) AS p WHERE
                                                    picks.quarterback=p.name AND picks.week=p.week AND picks.year=p.year)""")

    running_backs = connection.execute("""UPDATE picks, players
                                            SET picks.rb_points=(
                                                SELECT IFNULL(MAX(p.fantasy_points), 0) FROM (
                                                    SELECT * FROM players) AS p WHERE
                                                    picks.running_back=p.name AND picks.week=p.week AND picks.year=p.year)""")

    wide_receivers = connection.execute("""UPDATE picks, players
                                            SET picks.wr_points=(
                                                SELECT IFNULL(MAX(p.fantasy_points), 0) FROM (
                                                    SELECT * FROM players) AS p WHERE
                                                    picks.wide_receiver=p.name AND picks.week=p.week AND picks.year=p.year)""")

    tight_ends = connection.execute("""UPDATE picks, players
                                            SET picks.te_points=(
                                                SELECT IFNULL(MAX(p.fantasy_points), 0) FROM (
                                                    SELECT * FROM players) as p WHERE
                                                    picks.tight_end=p.name AND picks.week=p.week AND picks.year=p.year)""")

    defense = connection.execute("""UPDATE picks, defense
                                        SET picks.defense_points=defense.fantasy_points WHERE
                                        picks.defense=defense.team AND defense.week=picks.week AND defense.year=picks.year""")

    db.session.commit()
    connection.close()

def get_player_stats(year, week):
    games = nflgame.games(year, week)
    players = nflgame.combine_max_stats(games)
    for player in players:
        fantasy_points =    (player.passing_yds * .04 +
                    player.passing_tds * 4 -
                    player.passing_int +
                    player.rushing_yds * .1 +
                    player.rushing_tds * 6 +
                    player.receiving_yds * .1 +
                    player.kickret_tds * 6 +
                    player.receiving_tds * 6 +
                    (player.receiving_twoptm + player.rushing_twoptm + player.passing_twoptm) * 2 -
                    player.fumbles_lost * 2 +
                    player.fumbles_rec_tds * 6)

        two_point_conversions = player.receiving_twoptm + player.rushing_twoptm + player.passing_twoptm

        #

        try:
            p = Player(player.name, year, week, player.player.position, fantasy_points, player.passing_yds, player.passing_tds, player.passing_int,
                player.rushing_yds, player.rushing_tds, player.receiving_yds, player.receiving_tds, player.kickret_tds, two_point_conversions, player.fumbles_lost, player.fumbles_rec_tds)
        except AttributeError:
            p = Player(player.name, year, week, "N/A", fantasy_points, player.passing_yds, player.passing_tds, player.passing_int,
                player.rushing_yds, player.rushing_tds, player.receiving_yds, player.receiving_tds, player.kickret_tds, two_point_conversions, player.fumbles_lost, player.fumbles_rec_tds)

        db.session.add(p)
    db.session.commit()

def get_defense_score(year, week):

    teams = ["NE", "NYJ", "MIA", "BUF", "PIT", "BAL", "CLE", "CIN", "HOU", "IND", "JAX", "TEN", "DEN",
        "KC", "SD", "OAK", "DAL", "WSH", "NYG", "PHI", "MIN", "GB", "DET", "CHI", "NO", "TB", "ATL", "CAR", "SF", "SEA", "ARI", "STL"]

    games = nflgame.games(year, week)
    players = nflgame.combine_max_stats(games)

    for game in games:
        home_points = 0
        away_points = 0

        home_team = game.home
        home_points_allowed = game.score_away

        if home_points_allowed == 0:
            home_points += 10
        elif home_points_allowed < 7:
            home_points += 7
        elif home_points_allowed < 14:
            home_points += 4
        elif home_points_allowed < 21:
            home_points += 1
        elif home_points_allowed < 28:
            home_points += 0
        elif home_points_allowed < 35:
            home_points -= 1
        else:
            home_points -= 4

        away_team = game.away
        away_points_allowed = game.score_home

        if away_points_allowed == 0:
            away_points += 10
        elif away_points_allowed > 0 and away_points_allowed < 7:
            away_points += 7
        elif away_points_allowed > 6 and away_points_allowed < 14:
            away_points += 4
        elif away_points_allowed > 13 and away_points_allowed < 21:
            away_points += 1
        elif away_points_allowed > 20 and away_points_allowed < 28:
            away_points -= 0
        elif away_points_allowed > 27 and away_points_allowed < 35:
            away_points -= 1
        else:
            away_points -= 4

        for player in players.filter(team=home_team):
            home_points += (player.defense_sk +
                            player.defense_int * 2 +
                            #player.fumbles_rcv * 2 +
                            #player.fumbles_trcv * 2 +
                            player.defense_safe * 2 +
                            player.defense_ffum * 2 +
                            player.defense_tds * 6 +
                            player.defense_xpblk * 2 +
                            player.kickret_tds * 6 +
                            player.puntret_tds * 6)

        for player in players.filter(team=away_team):
            away_points += (player.defense_sk +
                            player.defense_int * 2 +
                            #player.fumbles_rcv * 2 +
                            #player.fumbles_trcv * 2 +
                            player.defense_safe * 2 +
                            player.defense_ffum * 2 +
                            player.defense_tds * 6 +
                            player.defense_xpblk * 2 +
                            player.kickret_tds * 6 +
                            player.puntret_tds * 6)

        home = Defense(home_team, week, year, home_points_allowed, home_points)
        away = Defense(away_team, week, year, away_points_allowed, away_points)
        db.session.add(home)
        db.session.add(away)

    db.session.commit()

def update_players(year, week):
    Player.query.filter_by(week=week, year=year).delete()
    get_player_stats(year, week)

def update_defense(year, week):
    Defense.query.filter_by(week=week, year=year).delete()
    get_defense_score(year, week)
