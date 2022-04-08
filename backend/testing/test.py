import requests



a = requests.get(url = "http://127.0.0.1:5000/api/datatypes")

print(a.json())


data = {
        "startblock" : 13481994,
        "endblock" : 13481994,
        "numresults" : 10,
        "finalblock" : 13481995,
        "increment" : 1}


a = requests.get(url = "http://127.0.0.1:5000/api/update", data = data)

print(a.json())
