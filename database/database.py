import sqlite3
import consts
import random
from pprint import pprint


class BotDatabase:
    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().execute("PRAGMA foreign_keys = 1")  # Enables foreign keys
        self.instantiate_db()

    def instantiate_db(self):
        """Method creates the database if they do not exist"""
        create_player_table = """CREATE TABLE IF NOT EXISTS players 
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

    def create_game(self, tuple_data, host_name):
        sql = "REPLACE INTO game (server, state, host_discord_id) VALUES (?,?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()
        game_data = self.get_active_game_data(tuple_data[0])
        self.create_player((game_data["game_id"], host_name, tuple_data[2], 1, "placeholder_role", "placeholder_alignment", 0, 0))

    def cancel_game(self, server):
        sql = "UPDATE game SET state = 'not_running' WHERE server = ?"
        count = self.conn.cursor().execute(sql, (server,))
        self.conn.commit()

    def create_player(self, tuple_data):
        sql = "REPLACE INTO players (game_id, name, discord_player_id, game_number, player_role, alignment, role_data, selected) VALUES (?,?,?,?,?,?,?,?)"
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()

    def remove_player(self, player_id):
        player_tuple = (player_id,)
        sql = "DELETE FROM players WHERE discord_player_id = ?"
        self.conn.cursor().execute(sql, player_tuple)
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

    def get_players_in_game(self, game_id):
        """Method gets all the regsitered users"""
        id_tuple = (game_id,)
        sql = "SELECT * FROM players WHERE game_id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, id_tuple)
        player_dicts = cur.fetchall()
        return player_dicts

    def set_new_host(self, server):
        server_tuple = (server,)
        game_id = self.get_active_game_data(server)["game_id"]
        id_tuple = (game_id,)
        sql = "SELECT * FROM players WHERE game_id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, id_tuple)
        player_dict = cur.fetchone()
        host_tuple = (player_dict["discord_player_id"], server)
        sql = "UPDATE game SET host_discord_id = ? WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, host_tuple)
        self.conn.commit()
        return player_dict

    def get_player_count(self, game_id):
        return len(self.get_players_in_game(game_id))

    def start_game(self, server, game_id):
        """sql = "UPDATE game SET state = ? WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, ("d1", server))
        self.conn.commit()
        """
        local_rolelist = consts.rolelist.copy()
        for i in range(consts.required_player_count):
            pick_alignment = local_rolelist.pop(random.randint(0,len(local_rolelist)-1))
            possible_roles = consts.allroles[pick_alignment]
            pick_role = random.choice(possible_roles)
            sql = "UPDATE players SET player_role = ?, alignment = ? WHERE game_id = ? AND game_number = ?"
            cur = self.conn.cursor()
            cur.execute(sql, (pick_role, pick_alignment, game_id, i + 1))
        self.conn.commit()
