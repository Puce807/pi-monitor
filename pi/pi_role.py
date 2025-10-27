
import requests

from config import *
from network import *

def run_pi():
    CLIENT_IP = get_client_ip()

    # Check if usb is working
    state = read_state()
    last = state

    while True:
        cur = read_state()
        if cur == "1":
            print("USB Up, Connected")
            send_message(CLIENT_IP, UDP_PORT, "connected")
            break
        time.sleep(1)

    # Main loop
    while True:
        time.sleep(POLLING_RATE)
        if not ping(CLIENT_IP, PING_PORT):
            print("No reply, trying to connect")
            if not ping(CLIENT_IP, PING_PORT, 5):
                print(f"Client ({CLIENT_IP}) disconnected, terminating program")
                break
        data = requests.get(f"http://{CLIENT_IP}:{DATA_PORT}").json()
        for x, y in data["cpu"]:
            print(f"{x}: {y}")