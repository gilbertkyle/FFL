#!/usr/bin/python

import datetime
import time
from app import Player, Defense, Pick, db
import get_players

base_week = datetime.datetime(2017, 8, 31, 10, 0, 0)
today = datetime.datetime.now()
diff = today - base_week
week = int(diff.days/7) if diff.days >= 0 else 0

# deletes the old player information for the current week, updates the players stats, updates the users scores, sleeps for 15 minutes, and repeats that cycle 60 times so it last for about 15 hours.


def main():
    for i in range(60):

        engine = db.engine
        connection = engine.connect()

        get_players.update_players(2017, week)
        get_players.update_defense(2017, week)

        get_players.update_picks(2017, week)
        connection.close()
        db.session.close()

        time.sleep(900)



if datetime.datetime.today().weekday() == 0 or datetime.datetime.today().weekday() == 3 or datetime.datetime.today().weekday() == 6:
    main()