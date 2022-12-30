import mysql.connector
from mysql.connector.errors import Error
import dbconfig as cfg

db = mysql.connector.connect(
    host=cfg.mysql["Host"],
    username = cfg.mysql["Username"],
    password = cfg.mysql["Password"],
    database = cfg.mysql["Database"]
)

def create_family_table():
    try:
        cursor = db.cursor()
        sql = "CREATE TABLE user_family (username VARCHAR(50) NOT NULL, password VARCHAR(50), balance float NOT NULL DEFAULT '0', debt float NOT NULL DEFAULT '0', PRIMARY KEY (username))"
        cursor.execute(sql)
        cursor.close()
    except Error as err:
        print("Error:", err)
        exit(1)

create_family_table()