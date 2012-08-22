import sqlite3

SQLDB = 'db/elixirs.db'

schema = open('sql/schema.sql').read()

conn = sqlite3.connect(SQLDB)
cursor = conn.cursor()
cursor.executescript(schema)

