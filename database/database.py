import sqlite3


class BotDatabase:
    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().execute("PRAGMA foreign_keys = 1")  # Enables foreign keys
        self.instantiate_db()

    def instantiate_db(self):
        """Method creates the database if they do not exist"""
        create_player_table = ("CREATE TABLE IF NOT EXISTS player_data "
                               "(game_id bigint NOT NULL, "
                               "name text NOT NULL, "
                               "player_id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT"
                               "discord_player_id bigint NOT NULL, "
                               "game_number integer NOT NULL, "
                               "role text NOT NULL, "
                               "aligntment text NOT NULL, "
                               "role_data integer NOT NULL, "
                               "selected integer NOT NULL)")
        create_prefix_table = ("CREATE TABLE IF NOT EXISTS prefixes "
                                 "(server bigint NOT NULL UNIQUE, "
                                 "prefix text NOT NULL,"
                                 "PRIMARY KEY(server))")
        create_active_game_table = ("CREATE TABLE IF NOT EXISTS game_data "
                                 "(server bigint NOT NULL UNIQUE, "
                                 "running boolean NOT NULL,"
                                 "state text NOT NULL,"
                                 "player_data_id bigint NOT NULL,"
                                 "PRIMARY KEY(server))")

        self.conn.cursor().execute(create_player_table)
        self.conn.cursor().execute(create_prefix_table)
        self.conn.cursor().execute(create_active_game_table)
        self.conn.commit()

    def change_prefix(self, tuple_data):
        """Method is used to register a user by taking a tuple of data to commit"""
        sql = "REPLACE INTO prefixes (prefix, server) VALUES (?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()

    def update_donation(self, tuple_data):
        """Method updates the donation of the registered users"""
        sql = ("INSERT INTO player_donation (update_date, coc_tag, coc_donation) "
               "VALUES (?,?,?)")
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
        sql = "SELECT * FROM game_data WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, server_tuple)
        data_dict = cur.fetchone()
        if data_dict == None:
            return None
        else:
            return data_dict
