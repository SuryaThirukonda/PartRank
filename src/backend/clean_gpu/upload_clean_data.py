import requests
import json

'''
response1 = requests.delete("http://localhost:8000/gpus/")

print(response1.status_code)
if (response1.status_code != 200):
    print("Failed to delete data. Status code: {response1.status_code}")
'''

with open("gpu_data_cleaned_2.json", "r") as f:
    gpus = json.load(f)


'''
for gpu in gpus:
    response = requests.post("http://localhost:8000/gpus/", json=gpu)
    print(response.status_code, response.text)

'''

print(len(gpus))
