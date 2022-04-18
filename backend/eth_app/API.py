#Api.py

"""

Call information from API and create lists with data stored for use in SQL

MISC: Some strange omissions of "to(or from)addresses" in some transactions in block #13481995, 
make sure the SQL database allows null inputs for everything

"""

import requests
import time
import mysql.connector
import os
import pandas

dbUser = os.environ.get('CLOUD_SQL_USERNAME')
dbPassword = os.environ.get('CLOUD_SQL_PASSWORD')
dbHost = os.environ.get('CLOUD_SQL_HOST')
dbName = os.environ.get('CLOUD_SQL_DATABASE_NAME')
apiKey = os.environ.get('ETHER_SCAN_API_KEY')

class Api():
    def __init__(self):
        
        self.blockNum, self.timeStamp, self.fromAdd, self.toAdd, self.value, self.gas, self.gasUsed = [], [], [], [], [], [], []
    
    def call(self, startBlock, endBlock, numResults):
        """ call Etherscan.io internal transactions API
        start block and end block (max range of 100 to ensure no data loss)
        numResults = number of transactions per call (max 10000)
        if startBlock to incBlock = n, increment should be n+1
        increment range by 101 to avoid duplicates, most recent block number as of writing this was at 14471993"""

        if (endBlock - startBlock) < 100:
            self.increment = (endBlock - startBlock)
        else:
            self.increment = 100
        
        self.running = True
        self.startBlock = startBlock
        self.endBlock = endBlock
        self.incBlock = self.increment + self.startBlock
        self.numResults = numResults
        
        while self.running == True:

            time.sleep(.25)

            if self.incBlock > self.endBlock:
                self.incBlock = self.endBlock
        
            self.call = {
                "module" : "account",
                "action" : "txlistinternal",
                "startblock" : f"{self.startBlock}",
                "endblock" : f"{self.incBlock}", 
                "page" : "1",
                "offset" : f"{self.numResults}",
                "sort" : "asc",
                "apikey" : f"{apiKey}",
                }
            
            self.a = requests.get("https://api.etherscan.io/api", data = self.call)
            
            #insert try logic
            self.responseDict = self.a.json()
            self.resultDicts = self.responseDict['result']
            
            self.resultDict = self.resultDicts[0]

            if self.incBlock >= self.endBlock:
                self.running = False
                    
            self.startBlock += self.increment + 1
            self.incBlock += self.increment + 1

    def display(self, startBlock, endBlock):
        """ set results in lists and print """

        for self.resultDict in self.resultDicts:
                self.timeStamp.append(self.resultDict['timeStamp'])
                self.blockNum.append(self.resultDict['blockNumber'])
                self.fromAdd.append(self.resultDict['from'])
                self.toAdd.append(self.resultDict['to'])
                self.value.append(self.resultDict['value'])
                self.gas.append(self.resultDict['gas'])
                self.gasUsed.append(self.resultDict['gasUsed'])
                
        print(f"Total Internal Transactions returned in Block Range #{startBlock}-{endBlock}: {len(self.resultDicts)}")

        for i in range(len(self.blockNum)):
            print(self.timeStamp[i])
            print(self.blockNum[i])
            print(self.fromAdd[i])
            print(self.toAdd[i])
            print(self.value[i])
            print(self.gas[i])
            print(self.gasUsed[i])  

    def pandaDF(self):
        """ get SQL data into a Pandas Data Frame and return """
        self.conn = mysql.connector.connect(user=dbUser, 
                                            password=dbPassword, 
                                            host=dbHost, 
                                            database=dbName)
        self.cursor = self.conn.cursor()
        self.dataFrame = pandas.read_sql_query('SELECT * FROM ethentry4', self.conn)
        self.conn.close()
        return self.dataFrame

    def dbStore(self):
        """ store data to SQL database """
        self.conn = mysql.connector.connect(user=dbUser, 
                                            password=dbPassword, 
                                            host=dbHost, 
                                            database=dbName)
        self.cursor = self.conn.cursor()

        for self.resultDict in self.resultDicts:
            
                self.query = ("INSERT INTO ethentry4 (timestamp, blocknumber, fromaddress, toaddress, ethvalue, gas, gasused)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s) ")
                self.vals = (self.resultDict['timeStamp'],
                            self.resultDict['blockNumber'],
                            self.resultDict['from'],
                            self.resultDict['to'],
                            self.resultDict['value'],
                            self.resultDict['gas'],
                            self.resultDict['gasUsed'])

                self.cursor.execute(self.query, self.vals)
                self.conn.commit()

        self.conn.close()

        

if __name__ == "__main__":
    
    run = Api()

    startBlock = 13481994
    endBlock = 13482094
    
    run.call(startBlock, endBlock, numResults = 100)
    run.display(startBlock, endBlock)
    run.dbStore()
    #run.dbGet()
