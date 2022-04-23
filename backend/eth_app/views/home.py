from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import g
from flask import render_template
from flask import request

from eth_app.db import get_connection, get_data, add_data
from eth_app.API import Api

import os
import pandas as pd
import numpy as np

API_KEY = os.getenv("API_KEY")

bp = Blueprint('home', __name__)

@bp.route("/")
def test():
    return render_template("index.html")
