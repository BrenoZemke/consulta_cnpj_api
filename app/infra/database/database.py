import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with open('schema.sql', 'r') as f:
        sql_script = f.read()
    db = get_db()
    db.cursor().executescript(sql_script)
    db.commit()