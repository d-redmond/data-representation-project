import mysql.connector
from mysql.connector.errors import Error
import dbconfig as cfg

class HouseholdDB:
    def init_connect_to_db(self):
        db = mysql.connector.connect(
            host = cfg.mysql['Host'],
            username = cfg.mysql['Username'],
            password = cfg.mysql['Password'],
            database = cfg.mysql["Database"],
            pool_name = cfg.mysql["pool_name"],
            pool_size = 10
        )
        return db

    def get_connection(self):
        db = mysql.connector.connect(
            pool_name=cfg.mysql["pool_name"]
        )
        return db

    def __init__(self):
        db = self.init_connect_to_db()
        db.close()

    def create_new_user(self, values):
        try:
            db = self.get_connection()
            cursor = db.cursor()
            sql = "INSERT INTO family_members (username, password, balance, debt) values (%s, %s, %f, %f)"
            cursor.execute(sql, values)
            cursor.close()
            db.commit()
            db.close()
            return
        except Error as err:
            print("Error:", err)
            exit(1)

    def update_family_members(self, values):
        try:
            db = self.get_connection()
            cursor = db.cursor()
            sql = "UPDATE family_members SET username = %s, password = %s, balance = %f, debt = %f WHERE username = %s"
            cursor.execute(sql, values)
            db.commit()
            db.close()
        except Error as err:
            print("Error:", err)

    def delete_family_members(self, username):
        try:
            db = self.get_connection()
            cursor = db.cursor()
            sql = "DELETE FROM family_members WHERE username = %s"
            values = (username,)
            cursor.execute(sql, values)
            db.commit()
            db.close()
        except Error as err:
            print("Error:", err)

householdDB = HouseholdDB()