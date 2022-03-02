import requests




data = {"module" : "account",
        "action" : "balance",
        "address" : "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae",
        "tag" : "latest",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

data = {"module" : "block",
        "action" : "getblockreward",
        "blockno" : "14264753",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

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
        "address" : "0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3",
        "startblock" : "0",
        "endblock" : "2702578",
        "page" : "1",
        "offset" : "10",
        "sort" : "asc",
        "apikey" : "QT8JPG7ZA46INM8J9C89BWZDKQBHKHRYU7"}

a = requests.post("https://api.etherscan.io/api", data = data)

#print(a.json())
for i in a.json()["result"]:
    print(i)
