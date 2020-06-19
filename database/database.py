import sqlite3


class BotDatabase:
    def __init__(self, db_filepath):
        self.conn = sqlite3.connect(db_filepath)
        self.conn.row_factory = sqlite3.Row
        self.conn.cursor().execute("PRAGMA foreign_keys = 1")  # Enables foreign keys
        self.instantiate_db()

    def instantiate_db(self):
        """Method creates the database if they do not exist"""
        create_player_table = ("CREATE TABLE IF NOT EXISTS coc_players "
                               "(coc_tag text NOT NULL, "
                               "coc_name text NOT NULL, "
                               "coc_th integer NOT NULL, "
                               "PRIMARY KEY(coc_tag))")
        create_prefix_table = ("CREATE TABLE IF NOT EXISTS prefixes "
                                 "(prefix text NOT NULL, "
                                 "server bigint NOT NULL,"
                                 "PRIMARY KEY(server))")

        self.conn.cursor().execute(create_player_table)
        self.conn.cursor().execute(create_prefix_table)
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
        sql = "SELECT prefix FROM prefixes WHERE server = ?"
        cur = self.conn.cursor()
        cur.execute(sql, server_tuple)
        prefix = cur.fetchone()
        if prefix == None:
            bot.dbconn.set_prefix(("/", server[0]))
            return "/"
        else:
            return prefix[server[0]]
