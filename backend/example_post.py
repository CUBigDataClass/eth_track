import requests

url = 'http://localhost:5000/api/ethelement'
data = {"points" : [
            {   'timestamp': 1,
                'blocknumber' : 2,
                'fromaddress' : 3,
                'toaddress' : 4,
                'ethvalue' : 5,
                'gas' : 6,
                'gasused' : 7}
            ]}


x = requests.post(url, json = data)

print(x.text)
