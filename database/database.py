import sqlite3
from pprint import pprint


class BotDatabase:
    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().execute("PRAGMA foreign_keys = 1")  # Enables foreign keys
        self.instantiate_db()

    def instantiate_db(self):
        """Method creates the database if they do not exist"""
        create_player_table = """CREATE TABLE IF NOT EXISTS player 
                               (player_id INTEGER PRIMARY KEY AUTOINCREMENT, 
							   game_id bigint NOT NULL, 
                               name text NOT NULL, 
                               discord_player_id bigint NOT NULL, 
                               game_number integer NOT NULL, 
                               player_role text NOT NULL, 
                               alignment text NOT NULL, 
                               role_data integer NOT NULL, 
                               selected integer NOT NULL)"""
        create_prefix_table = ("CREATE TABLE IF NOT EXISTS prefixes "
                                 "(server bigint NOT NULL UNIQUE, "
                                 "prefix text NOT NULL,"
                                 "PRIMARY KEY(server))")
        create_active_game_table = ("CREATE TABLE IF NOT EXISTS game "
                                 "(game_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                                 "server bigint NOT NULL UNIQUE, "
                                 "state text NOT NULL,"
                                 "host_discord_id bigint NOT NULL)")

        self.conn.cursor().execute(create_player_table)
        self.conn.cursor().execute(create_prefix_table)
        self.conn.cursor().execute(create_active_game_table)
        self.conn.commit()

    def change_prefix(self, tuple_data):
        """Method is used to register a user by taking a tuple of data to commit"""
        sql = "REPLACE INTO prefixes (prefix, server) VALUES (?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()

    def create_game(self, tuple_data):
        sql = "REPLACE INTO game (server, state, host_discord_id) VALUES (?,?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()

    def cancel_game(self, server):
        sql = "UPDATE game SET state = 'not_running' WHERE server = ?"
        count = self.conn.cursor().execute(sql, (server,))
        print(count.rowcount)
        self.conn.commit()

    def create_player(self, tuple_data):
        sql = "REPLACE INTO game (game_id, name, discord_player_id, game_number, player_role, alignment, role_data, selected) VALUES (?,?,?,?,?,?,?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()
        
    def get_prefix(self, server):
        """Method gets all the regsitered users"""
        server_tuple = (server,)
        sql = "SELECT * FROM prefixes WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, server_tuple)
        prefix = cur.fetchone()
        if prefix == None:
            self.change_prefix(("/", server))
            return "/"
        else:
            return prefix["prefix"]

    def get_active_game_data(self, server):
        """Method gets all the regsitered users"""
        server_tuple = (server,)
        sql = "SELECT * FROM game WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, server_tuple)
        data_dict = cur.fetchone()
        return data_dict
