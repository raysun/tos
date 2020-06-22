import sqlite3

SQLITE_FILE = 'bot_database.db'
con = sqlite3.connect(SQLITE_FILE)
cur = con.cursor()

TEST_SERVER_ID = 682073910279143489
CAREQ = 305791733453815818
RAY = 134153092378656769

def create_games():
    data = [
        [100, TEST_SERVER_ID, "waiting", CAREQ]
    ]
    query = """
    INSERT INTO game
    (game_id, server, state, host_discord_id)
    VALUES
    (?, ?, ?, ?)
    """

    cur.executemany(query, data)
    con.commit()

def create_players():
    data = [
        [100, TEST_SERVER_ID, "waiting", CAREQ]
    ]
    query = """
    INSERT INTO players
    (player_id, game_id, name, discord_player_id, game_number, player_role, alignment, role_data, selected)
    VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cur.executemany(query, data)
    con.commit()
