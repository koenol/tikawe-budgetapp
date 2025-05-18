import sqlite3
import os

if not os.path.exists("database.db"):
    db = sqlite3.connect("database.db")

    database_cursor = db.cursor()


    try:
        with open("schema.sql", "r") as schema:
            schema_file = schema.read()

            database_cursor.executescript(schema_file)

            db.commit()
            db.close()
    except FileNotFoundError:
        print("Files missing")

