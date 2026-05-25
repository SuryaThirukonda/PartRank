import time

import requests
from bs4 import BeautifulSoup
import json

url = "https://www.videocardbenchmark.net/mid_range_gpus.html"
url2 = "https://www.videocardbenchmark.net/high_end_gpus.html"

#act as browser to avoid being blocked by the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

def fetch_gpu_data(url):
    session = requests.Session()

    response = session.get(url, headers=headers, timeout=10)
    string = response.text
    if (response.status_code != 200):
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return ""
    return string

temp = fetch_gpu_data(url)


soup = BeautifulSoup(temp, "html.parser")
#gpu_names = soup.find_all("span", class_ = "prdname")
#gpu_price = soup.select("span.price-neww")
#gpu_performance = soup.select("span.mark-neww")
gpus = []

rows = soup.select('li[id^="pk"]')
print(len(rows))

for row in rows:
    ntemp = row.select_one("span.prdname")
    prtemp =row.select_one("span.price-neww")
    pertemp = row.select_one("span.mark-neww")

    name = ntemp.get_text(strip=True)
    performance = pertemp.get_text(strip=True).replace(',', '')
    try:
        performance = int(performance)
    except ValueError:
        print("som is wrong with performance", name, performance)
        break
    
    price = None
    if prtemp:
        price = prtemp.get_text(strip=True)
        if prtemp not in ("N/A", "NA", ""):
            clean = "".join(ch for ch in prtemp.get_text(strip=True) if ch.isdigit() or ch == ".")
            if clean:
                price = float(clean)
            else:
                price = None
    

    if (price == "N/A" or price == "NA" or price is None):
        gpus.append({"name": name, "performance": performance})
    else:
        gpus.append({"name": name, "price": price, "performance": performance})


for gpu in gpus:
    if "price" in gpu:
        req = requests.post("http://127.0.0.1:8000/gpus/", json={"name": gpu["name"], "price": gpu["price"], "performance": gpu["performance"]})
    else:
        req = requests.post("http://127.0.0.1:8000/gpus/", json={"name": gpu["name"], "performance": gpu["performance"]})
    print(req.status_code)
    time.sleep(0.01)



'''
for i in range(len(gpu_names)):
    name = gpu_names[i].text.strip()
    price = (gpu_price[i].text.strip())
    performance = int(gpu_performance[i].text.strip())
    if (price == "N/A" or price == "NA"):
        req = req = requests.post("http://127.0.0.1:8000/gpus/", json={"name": name, "performance": performance})
    else:
        price = float(price.replace("$", "").replace(",", "").replace(" ", "").replace("\n", "").replace("*", ""))
        req = requests.post("http://127.0.0.1:8000/gpus/", json={"name": name, "price": price, "performance": performance})
    print(req.status_code)
'''

#print(len(gpu_names), len(gpu_price), len(gpu_performance))

#print(temp)
#print(gpu_names[0].text.strip(), gpu_price[0].text.strip(), gpu_performance[0].text.strip())




