import sqlite3 as sq

connect = sq.connect("Steam.db")
cursor = connect.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS usuario(

    """
)