
import time

import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

url = "https://www.videocardbenchmark.net/GPU_mega_page.html"


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
gpus = []

print(temp[5000:6000])