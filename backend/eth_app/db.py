import os
import pymysql
from google.cloud.sql.connector import connector
from flask import jsonify


dbUser = os.environ.get('CLOUD_SQL_USERNAME')
dbPassword = os.environ.get('CLOUD_SQL_PASSWORD')
dbName = os.environ.get('CLOUD_SQL_DATABASE_NAME')
dbConnection = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
#apiKey = os.environ.get('ETHER_SCAN_API_KEY')
dbHost = os.environ.get("CLOUD_SQL_HOST")


def get_connection():
    socket = '/cloudsql/{}'.format(dbConnection)
    try:
        conn: pymysql.connections.Connection = connector.connect(
            os.environ["CLOUD_SQL_CONNECTION_NAME"],
            "pymysql",
            user=os.environ["CLOUD_SQL_USERNAME"],
            password=os.environ["CLOUD_SQL_PASSWORD"],
            db=os.environ["CLOUD_SQL_DATABASE_NAME"],
        )
    except pymysql.MySQLError as e:
        print(e)

    return conn

def get_data(startblock, endblock):
    print("GETTING DATA")
    conn = get_connection()
    with conn.cursor() as cursor:
        result = cursor.execute(f"SELECT * FROM ethelements WHERE blocknumber BETWEEN {startblock} AND {endblock};")
        data = cursor.fetchall()
        got_data = jsonify(data)
    conn.close()
    return got_data

def add_data(request):
    print("ADDING DATA")
    conn = get_connection()
    
    timestamp = request["timestamp"]
    blocknumber = request["blocknumber"]
    fromaddress = request["fromaddress"]
    toaddress = request["toaddress"]
    ethvalue = request["ethvalue"]
    gas = request["gas"]
    gasused = request["gasused"]

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO ethelements (timestamp, blocknumber, fromaddress, toaddress, ethvalue, gas, gasUsed) VALUES (%s, %s, %s, %s, %s, %s, %s)", (timestamp, blocknumber, fromaddress, toaddress, ethvalue, gas, gasused))

    conn.commit()
    conn.close()
