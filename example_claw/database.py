import os
import sqlite3

from flask import g

DATABASE = os.environ["EXAMPLE_CLAW_DATABASE_PATH"]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def refresh_corpus():
    import example_claw
    import importlib.resources as pkg_resources
    prefix_corpus = [
        (line,) for l in pkg_resources.read_text(example_claw, "prefix.txt").split("\n") if (line := l.strip().lower())
    ]
    suffix_corpus = [
        (line,) for l in pkg_resources.read_text(example_claw, "suffix.txt").split("\n") if (line := l.strip().lower())
    ]
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM prefixes")
    cur.execute("DELETE FROM suffixes")
    cur.executemany(f"INSERT INTO prefixes(prefix) VALUES (?)", prefix_corpus)
    cur.executemany(f"INSERT INTO suffixes(suffix) VALUES (?)", suffix_corpus)
    db.commit()
    cur.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
