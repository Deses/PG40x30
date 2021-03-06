# -*- coding: utf-8 -*-
import os
import sqlite3
from main import logger
from time import time


class DBwrapper(object):
    class __DBwrapper(object):
        dir_path = os.path.dirname(os.path.abspath(__file__))

        def __init__(self):
            database_path = os.path.join(self.dir_path, "pg4030_database.db")

            if not os.path.exists(database_path):
                logger.warning("File '" + database_path + "' does not exist! Trying to create one.")
                try:
                    self.create_database(database_path)
                except Exception as ex:
                    logger.error("An error has occurred while creating the database!", ex)

            self.connection = sqlite3.connect(database_path)
            self.connection.text_factory = lambda x: str(x, 'utf-8', "ignore")
            self.cursor = self.connection.cursor()

        @staticmethod
        def create_database(database_path: str) -> None:
            # Create database file and add admin and users table to the database
            open(database_path, 'a').close()

            connection = sqlite3.connect(database_path)
            connection.text_factory = lambda x: str(x, 'utf-8', "ignore")
            cursor = connection.cursor()

            # cursor.execute("CREATE TABLE 'admins' "
            #                "('userID' INTEGER NOT NULL,"
            #                "'name' TEXT,"
            #                "'tgUsername' TEXT,"
            #                "PRIMARY KEY('userID'));")

            cursor.execute("CREATE TABLE 'users'"
                           "('userID' INTEGER NOT NULL" + ","
                           "'first_name' TEXT" + ","
                           "'last_name' TEXT" + ","
                           "'username' TEXT NOT NULL" + ","
                           "'number' INTEGER NOT NULL" + ","
                           "'language_code' TEXT"
                           ");")

            cursor.execute("CREATE TABLE 'user_profile'"
                           "('alertID' INTEGER NOT NULL" + ","
                           "'userID' INTEGER NOT NULL" + ","
                           "'alert' NUMERIC" + ","
                           "PRIMARY KEY('alertID'));")

            connection.commit()
            connection.close()

        def add_user(self, userID: int, first_name: str, last_name: str, username: str, number: int, language_code: str) -> None:
            try:
                self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);",
                                    (userID, first_name, last_name, username, number, language_code))
                self.connection.commit()
            except sqlite3.IntegrityError as ex:
                logger.error("An error has occurred while adding an user!", ex)

        def get_user(self, user_id: int) -> tuple:
            self.cursor.execute("SELECT * FROM users WHERE userID=?;", [str(user_id)])

            result = self.cursor.fetchone()
            if result:
                if len(result) > 0:
                    return result
            return ()

        def get_all_users(self) -> list:
            self.cursor.execute("SELECT rowid, * FROM users ORDER BY number ASC;")
            return self.cursor.fetchall()

        def get_used_numbers(self) -> list:
            self.cursor.execute("SELECT number FROM users;")
            return self.cursor.fetchall()

        def add_user_profile(self, userID: int, alert: int) -> None:
            try:
                self.cursor.execute("INSERT INTO user_profile VALUES (userID, alert);",
                                    (userID, alert))
                self.connection.commit()
            except sqlite3.IntegrityError as ex:
                logger.error("An error has occurred while adding user info!", ex)

        # def update_user_profile(self, value: str, user_id: int) -> None:
        #     self.cursor.execute("UPDATE user_profile SET alert = ? WHERE userID = ?;",
        #                         [value, str(user_id)])
        #     self.connection.commit()

        def get_user_profile(self) -> list:
            self.cursor.execute("SELECT rowid, * FROM user_profile JOIN users USING(userID) ORDER BY number ASC;")
            return self.cursor.fetchall()
        # def get_recent_players(self):
        #     one_day_in_secs = 60 * 60 * 24
        #     current_time = int(time())
        #     self.cursor.execute("SELECT userID FROM users WHERE lastPlayed>=?;", [current_time - one_day_in_secs])
        #
        #     return self.cursor.fetchall()
        #
        # def get_played_games(self, user_id: int) -> int:
        #     self.cursor.execute("SELECT gamesPlayed FROM users WHERE userID=?;", [str(user_id)])
        #
        #     result = self.cursor.fetchone()
        #
        #     if not result:
        #         return 0
        #
        #     if len(result) > 0:
        #         return int(result[0])
        #     else:
        #         return 0



        # def get_admins(self) -> list:
        #     self.cursor.execute("SELECT userID from admins;")
        #     admins = self.cursor.fetchall()
        #     admin_list = []
        #     for admin in admins:
        #         admin_list.append(admin[0])
        #     return admin_list

        def get_lang_id(self, user_id: int) -> str:
            self.cursor.execute("SELECT languageID FROM users WHERE userID=?;", [str(user_id)])
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return "en"



        def insert(self, column_name: str, value: str, user_id: int) -> None:
            self.cursor.execute("UPDATE users SET " + column_name + "= ? WHERE userID = ?;",
                                [value, str(user_id)])
            self.connection.commit()

        def is_user_saved(self, user_id: int) -> bool:
            self.cursor.execute("SELECT rowid, * FROM users WHERE userID=?;", [str(user_id)])

            result = self.cursor.fetchall()
            if len(result) > 0:
                return True
            else:
                return False

        # def user_data_changed(self, user_id: int, first_name: str, last_name: str, username: str) -> bool:
        #     self.cursor.execute("SELECT * FROM users WHERE userID=?;", [str(user_id)])
        #
        #     result = self.cursor.fetchone()
        #
        #     # check if user is saved
        #     if result:
        #         if result[2] == first_name and result[3] == last_name and result[4] == username:
        #             return False
        #         return True
        #     else:
        #         return True
        #
        # def update_user_data(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        #     self.cursor.execute("UPDATE users SET first_name=?, last_name=?, username=? WHERE userID=?;",
        #                         (first_name, last_name, username, str(user_id)))
        #     self.connection.commit()
        # 
        # def reset_stats(self, user_id: int) -> None:
        #     self.cursor.execute(
        #         "UPDATE users SET gamesPlayed='0', gamesWon='0', gamesTie='0', lastPlayed='0' WHERE userID=?;",
        #         [str(user_id)])
        #     self.connection.commit()

        def close_conn(self) -> None:
            self.connection.close()

    instance = None

    def __init__(self):
        if not DBwrapper.instance:
            DBwrapper.instance = DBwrapper.__DBwrapper()

    @staticmethod
    def get_instance() -> __DBwrapper:
        if not DBwrapper.instance:
            DBwrapper.instance = DBwrapper.__DBwrapper()

        return DBwrapper.instance