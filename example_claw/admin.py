from flask import Blueprint
import http

bp = Blueprint("auth", __name__, url_prefix="/admin")


@bp.route("/ping")
def ping():
    return ("", http.HTTPStatus.NO_CONTENT)
