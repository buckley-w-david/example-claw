import os
from functools import wraps
import uuid
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import http

from example_claw.database import get_db, query_db, refresh_corpus

bp = Blueprint("admin", __name__, url_prefix="/admin")
auth = HTTPBasicAuth()
users = {
    'admin': generate_password_hash(os.environ["EXAMPLE_CLAW_ADMIN_PASSWORD"])
}

@bp.route("/ping")
def ping():
    return ("", http.HTTPStatus.NO_CONTENT)

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password): # type: ignore
        return username

def verify_csrf(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if session["csrf_token"] != request.form.get("csrf_token", None):
            flash("Invalid CSRF token!")
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return inner


@bp.route("/")
@auth.login_required
def index():
    csrf_token = str(uuid.uuid4())
    session["csrf_token"] = csrf_token
    prefixes = query_db("SELECT prefix FROM prefixes ORDER BY prefix")
    suffixes = query_db("SELECT suffix FROM suffixes ORDER BY suffix")
    return render_template('admin/index.html', prefixes=prefixes, suffixes=suffixes, csrf_token=csrf_token)


@bp.route("/prefix", methods=("POST",))
@auth.login_required
@verify_csrf
def add_prefix():
    prefix = request.form['prefix']
    db = get_db()
    cur = db.execute("INSERT INTO prefixes(prefix) VALUES (?)", (prefix,))
    db.commit()
    cur.close()
    flash("Success!")
    return redirect(url_for('admin.index'))

@bp.route("/prefix/<prefix>/delete", methods=("POST",))
@auth.login_required
@verify_csrf
def delete_prefix(prefix: str):
    db = get_db()
    cur = db.execute("DELETE FROM prefixes WHERE prefix=?", (prefix,))
    db.commit()
    cur.close()
    flash("Removed %s!" % prefix)
    return redirect(url_for('admin.index'))

@bp.route("/suffix", methods=("POST",))
@auth.login_required
@verify_csrf
def add_suffix():
    suffix = request.form['suffix']
    db = get_db()
    cur = db.execute("INSERT INTO suffixes(suffix) VALUES (?)", (suffix,))
    db.commit()
    cur.close()
    flash("Success!")
    return redirect(url_for('admin.index'))

@bp.route("/suffix/<suffix>/delete", methods=("POST",))
@auth.login_required
@verify_csrf
def delete_suffix(suffix: str):
    db = get_db()
    cur = db.execute("DELETE FROM suffixes WHERE suffix=?", (suffix,))
    db.commit()
    cur.close()
    flash("Removed %s!" % suffix)
    return redirect(url_for('admin.index'))

@bp.route("/refresh", methods=("POST",))
@auth.login_required
@verify_csrf
def refresh():
    refresh_corpus()
    flash("Refreshed!")
    return redirect(url_for('admin.index'))
