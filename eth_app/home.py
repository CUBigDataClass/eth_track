from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from eth_app.auth import login_required
from eth_app.db import get_db

bp = Blueprint('home', __name__, url_prefix="/home")

@bp.route('/')
def index():
    db = get_db()
    datatypes = db.execute(
        'SELECT p.id, title, units, description'
        ' FROM datatype p'
    ).fetchall()
    return render_template('home/index.html', datatypes=datatypes)
