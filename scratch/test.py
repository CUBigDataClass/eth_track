import requests
import time








data = {"address" : "0xf663F4b30dD18546cb71a607b7a89a36e92a244C",
        "module" : "contract",
        "action" : "getabi",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

data = {
   "module" : "contract",
   "action" : "getsourcecode",
   "address" : "0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413",
    "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

data = {"module" : "transaction",
       "action" : "getstatus",
       "txhash" : "0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76",
       "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

data = {
        "module" : "account",
        "action" : "tokennfttx",
        "contractaddress" : "0x06012c8cf97bead5deae237070f9587f8e7a266d",
        "address" : "0x6975be450864c02b4613023c2152ee0743572325",
        "page" : "1",
        "offset" : "100",
        "startblock" : "0",
        "endblock" : "27025780",
        "sort" : "asc",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

data = {
        "module" : "account",
        "action" : "txlistinternal",
        "startblock" : "0",
        "endblock" : "2702578",
        "address" : "0xCAf96BdB5e3e936dFbD8F1224C4d78740e9b4531",
        "page" : "1",
        "offset" : "10",
        "sort" : "asc",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}



data = {"module" : "block",
        "action" : "getblockreward",
        "blockno" : "14264753",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

start = time.time()
a = requests.post("https://api.etherscan.io/api", data = data)
print(time.time() - start)

print(a.json())






















