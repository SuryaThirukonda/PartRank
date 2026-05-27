import requests
import json

'''
response1 = requests.delete("http://localhost:8000/gpus/")

print(response1.status_code)
if (response1.status_code != 200):
    print("Failed to delete data. Status code: {response1.status_code}")
'''


with open("..\\data\\gpu_data_cleaned_6_priced.json", "r") as f:
    gpus = json.load(f)
    '''
    count = 0
    for gpu in gpus:
        if "price" in gpu:
            print(gpu["name"], gpu["price"], gpu["performance"])
            count+=1
    print(len(gpus), " actual price", count)
    '''




for gpu in gpus:
    response = requests.post("http://localhost:8000/gpus/", json=gpu)
    print(response.status_code, response.text)



