import requests


with open("gpu_data.json", "w") as j:
    response = requests.get("http://localhost:8000/gpus/?skip=0&limit=1500")
    j.write(response.text)
    