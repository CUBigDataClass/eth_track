from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from eth_app.db import get_db

bp = Blueprint('home', __name__, url_prefix="/home")

@bp.route('/')
def index():

    # Access the local copy of the database here
    db = get_db()

    # An example of passing python data from the database to the html page
    datatypes = db.execute(
        'SELECT p.id, title, units, description'
        ' FROM datatype p'
    ).fetchall()

    # datatypes is a python dict returned from db
    # you can send this data to html (see templates/home/index.html)
    # and access the data there
    return render_template('home/index.html', datatypes=datatypes)
