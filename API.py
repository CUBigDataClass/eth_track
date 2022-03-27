"""

Call information from API and create lists with data stored for use in SQL

MISC: Some strange omissions of "to(or from)addresses" in some transactions in block #13481995

"""

import requests, time, json

class Api():
    def __init__(self):
        
        self.blockNum, self.fromAdd, self.toAdd, self.value, self.gas, self.gasUsed = [], [], [], [], [], []
    
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
            
            for self.resultDict in self.resultDicts:
                self.blockNum.append(self.resultDict['blockNumber'])
                self.fromAdd.append(self.resultDict['from'])
                self.toAdd.append(self.resultDict['to'])
                self.value.append(self.resultDict['value'])
                self.gas.append(self.resultDict['gas'])
                self.gasUsed.append(self.resultDict['gasUsed'])
                
            print(f"Total Internal Transactions returned in Block Range #{self.startBlock}-{self.endBlock}: {len(self.resultDicts)}")
                    
            self.startBlock += increment
            self.endBlock += increment
            
            if self.startBlock == finalBlock:
                self.running = False
    
    def display(self):
        """ check results and print, or store in SQL database """
        for i in range(len(self.blockNum)):
            print(self.blockNum[i])
            print(self.fromAdd[i])
            print(self.toAdd[i])
            print(self.value[i])
            print(self.gas[i])
            print(self.gasUsed[i])  


if __name__ == "__main__":
    
    run = Api()
    
    
    run.call(13481994, 13481994, numResults = 10, finalBlock = 13481997, increment = 1)
    run.display()