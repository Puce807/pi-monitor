
import time
from UDP import *
from utils import get_client_ip

CLIENT_IP = get_client_ip()

state = read_state()
if state == "1":
    print("Interface Up!")
    send_message(CLIENT_IP, 5005, "connected")

last = state
print(f"Watching usb0, initial state = {last}")

while True:
    cur = read_state()
    if cur != last:
        if cur == "1":
            print("Interface Up!")
            send_message(CLIENT_IP, 5005, "connected")
    time.sleep(1)