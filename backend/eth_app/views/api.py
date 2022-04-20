from flask import Blueprint
from flask import current_app
from flask import jsonify
from flask import g
from flask import request

from eth_app.db import get_connection, get_data, add_data
from eth_app.API import Api

import os
import pandas as pd
import numpy as np

API_KEY = os.getenv("API_KEY")

bp = Blueprint('api', __name__)

@bp.route("/test")
def test():
    return "hello world"


def get_new_blocks_from_api(blocks_to_get):
    response = pd.DataFrame({"timestamp" : [], "blocknumber" : [], "fromaddress" : [], "toaddress" : [], 
                "ethvalue" : [], "gas" : [], "gasused" : []})

    # Add all the data that wasn't returned by the database
    for block in blocks_to_get:

        # The function call to get data externally
        retrieved_data = get_api_data(block)

        # Add each new data point to the database
        for i in range(len(retrieved_data["timestamp"])):
            t = retrieved_data["timestamp"][i]
            b = retrieved_data["blocknumber"][i]
            f = retrieved_data["fromaddress"][i]
            to = retrieved_data["toaddress"][i]
            e = retrieved_data["ethvalue"][i]
            g = retrieved_data["gas"][i]
            gu = retrieved_data["gasused"][i]
            indata = {"timestamp" : t, "blocknumber" : b, "fromaddress" : f, "toaddress" : to,
                        "ethvalue" : e, "gas" : g, "gasused" : gu}

            # Add the new data to the database
            add_data(indata)

        # Concat the response with this new data
        
        response = pd.concat([response, pd.DataFrame(retrieved_data)])

    return response

def get_raw_blocks_from_database(startblock, endblock):

    # The raw output of select in range from the database - some may be missing!
    data = get_data(startblock, endblock)

    # The return dict unfiltered
    response = {"timestamp" : [], "blocknumber" : [], "fromaddress" : [], "toaddress" : [], 
                "ethvalue" : [], "gas" : [], "gasused" : []}

    if len(data.json) > 0: # The database actuall had some hits
        # The blocks the database did return
        blocks = np.array(data.json)[:,1].astype(int)
        max_block_ret = blocks.max()
        min_block_ret = blocks.min()
        blocks = set(np.arange(min_block_ret, max_block_ret + 1).astype(int))
        # The blocks the database did not return in this range
        toget = set(np.arange(startblock, endblock + 1).astype(int)) - blocks
        # Add all the data that was returned by the database
        for pt in data.json:
            ti, b, f, to, e, g, gu = pt
            response["timestamp"].append(ti)
            response["blocknumber"].append(b)
            response["fromaddress"].append(f)
            response["toaddress"].append(to)
            response["ethvalue"].append(e)
            response["gas"].append(g)
            response["gasused"].append(gu)

    else: # The database didn't have any hits
        toget = np.arange(startblock, endblock + 1)

    return pd.DataFrame(response), np.array(list(toget))

def get_api_data(block):
    api = Api()
    api.call(block, block)

    data = {"timestamp" : [], "blocknumber" : [], "fromaddress" : [], "toaddress" : [],
            "ethvalue" : [], "gas" : [], "gasused" : []}

    for i in api.resultDicts:
        data["timestamp"].append(float(i["timeStamp"]))
        data["blocknumber"].append(float(i["blockNumber"]))
        data["fromaddress"].append(str(i["from"]))
        data["toaddress"].append(str(i["to"]))
        data["gas"].append(float(i["gas"]))
        data["gasused"].append(float(i["gasUsed"]))
        data["ethvalue"].append(float(i["value"]))

    return data


@bp.route("/ethelement", methods=["POST", "GET"])
def ethelement():
    if request.method == "POST":
        if not request.is_json:
            return jsonify({"msg" : "Missing JSON in request"}), 400
        for i in request.get_json()["points"]:
            add_data(i)
        return "added"

    else:
        startblock = request.args.get("startblock")
        endblock = request.args.get("endblock")

        if startblock == None or endblock == None:
            return jsonify({"msg" : "Missing Startblock and or endblock parameters"}), 400

        try:
            startblock = int(startblock)
            endblock = int(endblock)
        except:
            return jsonify({"msg" : "Invalid datatype for startblock or endblock"}), 400

        df1, toget = get_raw_blocks_from_database(startblock, endblock)
        df2 = get_new_blocks_from_api(toget)
        response = pd.concat([df1, df2])

        return jsonify(response.to_dict("list"))


@bp.route("/ethelementfiltered", methods=["GET"])
def ethelementfiltered():
    # Same as unfiltered
    startblock = request.args.get("startblock")
    endblock = request.args.get("endblock")
    numresults = request.args.get("numresults")

    if startblock == None or endblock == None or numresults == 0:
        return jsonify({"msg" : "Missing Startblock and or endblock parameters"}), 400

    try:
        startblock = int(startblock)
        endblock = int(endblock)
        numresults = int(numresults)
    except:
        return jsonify({"msg" : "Invalid datatype for startblock or endblock"}), 400

    df1, toget = get_raw_blocks_from_database(startblock, endblock)
    df2 = get_new_blocks_from_api(toget)
    df = pd.concat([df1, df2])

    # Get only the blocks in range (THIS DOESN"T DO ANYTHING!)
    df = df[(df["blocknumber"] <= endblock) & (df["blocknumber"] >= startblock)]

    # All the unique addresses
    addresses = list(set(df["fromaddress"].unique()) | set(df["toaddress"].unique()))

    # Filtered response
    data = {"address" : [], "Volume" : [], "Gas" : [], "Eth" : [], "GasUsed" : []}

    for address in addresses:
        data["address"].append(address)
        subset = df[(df["fromaddress"] == address) | (df["toaddress"] == address)]
        volume = len(subset)
        s = subset.sum()
        
        data["Volume"].append(volume)
        data["Gas"].append(s.gas)
        data["Eth"].append(s.ethvalue)
        data["GasUsed"].append(s.gasused)
        
        
    df_ = pd.DataFrame(data)
    df_[["v_rank", "g_rank", "gu_rank", "e_rank"]] = 0
    df_.loc[df_.sort_values("Volume", ascending = False).index, "v_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("Gas", ascending = False).index, "g_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("Eth", ascending = False).index, "e_rank"] = np.arange(len(df_))
    df_.loc[df_.sort_values("GasUsed", ascending = False).index, "gu_rank"] = np.arange(len(df_))

    ret = {"Data" : []}
    for _, data in df_.iterrows():
        if data.g_rank < numresults or data.v_rank < numresults or data.e_rank < numresults or data.gu_rank < numresults:
            pt = {}
            pt["address"] = str(data.address)
            pt["Gas"] = {"Magnitude" : int(data.Gas), "Rank" : int(data.g_rank)}
            pt["Volume"] = {"Magnitude" : int(data.Volume), "Rank" : int(data.v_rank)}
            pt["Eth"] = {"Magnitude" : int(data.Eth), "Rank" : int(data.e_rank)}
            pt["GasUsed"] = {"Magnitude" : int(data.GasUsed), "Rank" : int(data.gu_rank)}
            ret["Data"].append(pt)
    ret["addresses"] = [str(a) for a in addresses]

    return jsonify(ret)
