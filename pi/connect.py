import time
import requests

import config

while True:
    data = requests.get("http://127.0.0.1:5000").json()

    for x, y in data.items():
        print(f"{x}: {y}")

    time.sleep(config.POLLING_RATE)