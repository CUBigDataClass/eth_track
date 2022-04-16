from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import g
from flask import request

from eth_app.db import get_db
from eth_app.API import Api

import os
import pandas as pd
import numpy as np

API_KEY = os.getenv("API_KEY")

bp = Blueprint('api', __name__)

@bp.route("/getdata")
def updateeth():
    start_block = int(request.args.get("startblock"))
    end_block = int(request.args.get("endblock"))

    api = Api()
    api.call(start_block, end_block, 10000)
    
    """
    # CHANGE THIS
    df = pd.read_csv("./test.csv")
    df = df[(df["blocknumber"] <= end_block) & (df["blocknumber"] >= start_block)]

    addresses = list(set(df["fromaddress"].unique()) | set(df["toaddress"].unique()))

    data = {"address" : [], "Volume" : [], "Gas" : [], "Eth" : [], "GasUsed" : []}

    for address in addresses:
        data["address"].append(address)
        subset = df[(df["fromaddress"] == address) | (df["toaddress"] == address)]
        volume = len(subset)
        s = subset.sum()
        
        data["Volume"].append(volume)
        data["Gas"].append(s.gas)
        data["Eth"].append(s.ethvalue)
        data["GasUsed"].append(s.gasUsed)
        
        
    df_ = pd.DataFrame(data)
    df_[["v_rank", "g_rank", "gu_rank", "e_rank"]] = 0
    df_.loc[df_.sort_values("Volume").index, "v_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("Gas").index, "g_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("Eth").index, "e_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("GasUsed").index, "gu_rank"] = np.arange(len(df_))

    ret = {"Data" : []}
    for i, data in df_.iterrows():
        pt = {}
        pt["address"] = int(data.address)
        pt["Gas"] = {"Magnitude" : int(data.Gas), "Rank" : int(data.g_rank)}
        pt["Volume"] = {"Magnitude" : int(data.Volume), "Rank" : int(data.v_rank)}
        pt["Eth"] = {"Magnitude" : int(data.Eth), "Rank" : int(data.e_rank)}
        pt["GasUsed"] = {"Magnitude" : int(data.GasUsed), "Rank" : int(data.gu_rank)}
        ret["Data"].append(pt)
    ret["addresses"] = [int(a) for a in addresses]

    return jsonify(ret)
    """

    return "hello"
