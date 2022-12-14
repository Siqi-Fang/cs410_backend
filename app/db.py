import sqlite3
from flask import current_app, g
from decouple import config
DB = config('DB')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB)
        print('opening {}'.format(DB))
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    connection = get_db()
    with current_app.open_resource('schema.sql') as f:
        connection.executescript(f.read())


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

