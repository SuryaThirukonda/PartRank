import requests
import json

#req = requests.post("http://127.0.0.1:8000/gpus/", json={"name":"RTX 4090","price":1599.99,"performance":100})
# print(req.status_code)

#req2 = requests.delete("http://127.0.0.1:8000/gpus/1")
#req3 = requests.delete("http://127.0.0.1:8000/gpus/2")
#req4 = requests.delete("http://127.0.0.1:8000/gpus/3")
#req5 = requests.delete("http://127.0.0.1:8000/gpus/4")
#req = requests.delete("http://127.0.0.1:8000/gpus/5")

req = requests.delete("http://127.0.0.1:8000/gpus/")


print (req.status_code)