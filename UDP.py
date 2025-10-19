
import os
import socket
import time

def read_state(IFACE="usb0"):
    try:
        with open(f"/sys/class/net/{IFACE}/carrier") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0"

def send_message(IP, PORT, MESSAGE):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if isinstance(MESSAGE, str):
            MESSAGE = MESSAGE.encode()
        sock.sendto(MESSAGE, (IP, PORT))
    finally:
        sock.close()

def start_listener(ip, port, callback):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Listening on {ip}:{port}...")
    while True:
        data, addr = sock.recvfrom(1024)
        callback(data.decode(), addr)
