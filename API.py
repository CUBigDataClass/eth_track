#Api.py

"""

Call information from API and create lists with data stored for use in SQL

MISC: Some strange omissions of "to(or from)addresses" in some transactions in block #13481995

"""

import requests
import time
import json
import mysql.connector
import os
from flask import jsonify


dbUser = os.environ.get('CLOUD_SQL_USERNAME')
dbPassword = os.environ.get('CLOUD_SQL_PASSWORD')
dbHost = os.environ.get('CLOUD_SQL_HOST')
dbName = os.environ.get('CLOUD_SQL_DATABASE_NAME')


class Api():
    def __init__(self):
        
        self.blockNum, self.timeStamp, self.fromAdd, self.toAdd, self.value, self.gas, self.gasUsed = [], [], [], [], [], [], []
    
    def call(self, startBlock, endBlock, numResults, finalBlock, increment):
        """ call Etherscan.io internal transactions API
        start block and end block (max range of 100 to ensure no data loss)
        numResults = number of transactions per call (max 10000)
        increment range by 101 to avoid duplicates, final blocks as of writing this at 14471993"""
        
        self.running = True
        self.startBlock = startBlock
        self.endBlock = endBlock
        self.numResults = numResults
        
        while self.running == True:
            
            time.sleep(.25)
        
            self.call = {
                "module" : "account",
                "action" : "txlistinternal",
                "startblock" : f"{self.startBlock}",
                "endblock" : f"{self.endBlock}", 
                "page" : "1",
                "offset" : f"{self.numResults}",
                "sort" : "asc",
                "apikey" : "EV9GPRDYRMVKQGSI9ZFWAHV5W2Q96IRSPA",
                }
            
            self.a = requests.get("https://api.etherscan.io/api", data = self.call)
            self.responseDict = self.a.json()
            self.resultDicts = self.responseDict['result']
            
            self.resultDict = self.resultDicts[0]
                    
            self.startBlock += increment
            self.endBlock += increment
            
            if self.startBlock == finalBlock:
                self.running = False

    def display(self):
        """ set results in lists and print """

        for self.resultDict in self.resultDicts:
                self.timeStamp.append(self.resultDict['timeStamp'])
                self.blockNum.append(self.resultDict['blockNumber'])
                self.fromAdd.append(self.resultDict['from'])
                self.toAdd.append(self.resultDict['to'])
                self.value.append(self.resultDict['value'])
                self.gas.append(self.resultDict['gas'])
                self.gasUsed.append(self.resultDict['gasUsed'])
                
        print(f"Total Internal Transactions returned in Block Range #{self.startBlock}-{self.endBlock}: {len(self.resultDicts)}")

        for i in range(len(self.blockNum)):
            print(self.timeStamp[i])
            print(self.blockNum[i])
            print(self.fromAdd[i])
            print(self.toAdd[i])
            print(self.value[i])
            print(self.gas[i])
            print(self.gasUsed[i])  
    
    def dbGet(self):
        """ GET from SQL database """
        self.conn = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbName)
        self.cursor = self.conn.cursor()
        self.result = self.cursor.execute('SELECT * FROM test;')
        self.test = self.cursor.fetchall()
        
        return jsonify(self.test)


    def dbStore(self):
        """ store data to SQL database """
        self.conn = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbName)
        self.cursor = self.conn.cursor()

        for self.resultDict in self.resultDicts:
            self.query = ("INSERT INTO test (timeStamp, blockNumber, from, to, value, gas, gasUsed)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE NOT EXISTS ")
            self.vals = (self.resultDict['timeStamp'],
                        self.resultDict['blockNumber'],
                        self.resultDict['from'],
                        self.resultDict['to'],
                        self.resultDict['value'],
                        self.resultDict['gas'],
                        self.resultDict['gasUsed'])

            self.cursor.execute(self.query, self.vals)
            self.conn.commmit()
        self.cursor.close()
        self.conn.close()

        

if __name__ == "__main__":
    
    run = Api()
    
    run.call(13481994, 13481994, numResults = 10, finalBlock = 13481997, increment = 1)
    run.display()
    run.dbStore()
    #run.dbGet()