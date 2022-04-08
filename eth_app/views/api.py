from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import g
from flask import request

from eth_app.db import get_db
from eth_app.eth_data import API

import os

API_KEY = os.getenv("API_KEY")

bp = Blueprint('api', __name__)

@bp.route("/datatypes", methods = ["GET"])
def datatypes():
    db = get_db()
    datatypes = db.execute(
        'SELECT p.id, title, units, description'
        ' FROM datatype p'
    ).fetchall()

    data = []

    for row in datatypes:
        d = {}
        d["id"] = row["id"]
        d["Title"] = row["title"]
        d["Units"] = row["units"]
        d["Description"] = row["description"]
        data.append(d)
    return jsonify(data)

@bp.route("/getdata", methods = ["GET", "POST"])
def call():
    data = "hello world"
    print(dict(g))
    return jsonify({"data" : data})

def eth_update(start_block, end_block, num_results, final_block, increment):
    run = API(API_KEY)
    run.call(start_block, end_block, num_results, final_block, increment)
    run.display()


#example.com?arg1=value1&arg2=value2


@bp.route("/update")
def updateeth():
    start_block = request.args.get("startblock")
    end_block = request.args.get("endblock")
    num_results = request.args.get("numresults")
    final_block = request.args.get("finalblock")
    increment = request.args.get("increment")

    print(start_block, end_block, num_results, final_block, increment)
    eth_update(start_block, end_block, num_results, final_block, increment)
