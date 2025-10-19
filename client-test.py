
from network import *

def on_message(data="", addr=""):
    ip, port = addr
    print(f"Message: {data}")
    print(f"From {ip} on port {port}")
    ping_responder()

start_listener("0.0.0.0", 5005, on_message, True)



