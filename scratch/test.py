import requests
import time

apikey = "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"
startblock=13481774
endblock=startblock
numresults = 10

call = {
    "module" : "account",
    "action" : "txlistinternal",
    "startblock" : f"{startblock}",
    "endblock" : f"{endblock}", 
    "sort" : "asc",
    "apikey" : f"{apikey}",
}

print(call) 
a = requests.get("https://api.etherscan.io/api", data = call)

#insert try logic
print(a.json())
print(len(a.json()["result"]))


test_url = "http://localhost:5000/api/ethelementfiltered?startblock=14623760&endblock=14623960&numresults=10"
