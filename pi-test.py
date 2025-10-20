
import time
import requests
from network import *
from utils import get_client_ip

CLIENT_IP = get_client_ip()

state = read_state()

last = state
print(f"Watching usb0, initial state = {last}")

while True:
    cur = read_state()
    if cur == "1":
        print("Interface Up!")
        send_message(CLIENT_IP, 5005, "connected")
        break
    time.sleep(1)

while True:
    if not ping(CLIENT_IP, 5006):
        print("Lost Connection, trying to connect")
        if not ping(CLIENT_IP, 5006, 5):
            print(f"Client {CLIENT_IP} disconnected, terminating program")
            break
    data = requests.get(f"{CLIENT_IP}:5000").json()

    for x, y in data["cpu"].items():
        print(f"{x}: {y}")

    time.sleep(5)